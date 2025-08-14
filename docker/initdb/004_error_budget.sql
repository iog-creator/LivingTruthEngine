-- Error Budget & Recovery Automation Schema
-- Phase 9.5.5 - Error Budgeting & Recovery Automation

-- Create error budget metrics table
CREATE TABLE IF NOT EXISTS lte.error_budget_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    service_name VARCHAR(100) NOT NULL,
    metric_type VARCHAR(50) NOT NULL, -- 'availability', 'latency', 'error_rate'
    metric_value DECIMAL(10,6) NOT NULL,
    slo_target DECIMAL(10,6) NOT NULL,
    error_budget_consumed DECIMAL(10,6) NOT NULL,
    error_budget_remaining DECIMAL(10,6) NOT NULL,
    window_start TIMESTAMP WITH TIME ZONE NOT NULL,
    window_end TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create recovery actions table
CREATE TABLE IF NOT EXISTS lte.recovery_actions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    action_type VARCHAR(100) NOT NULL, -- 'container_restart', 'cache_purge', 'db_reset'
    service_name VARCHAR(100) NOT NULL,
    trigger_reason TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    duration_ms INTEGER,
    error_message TEXT,
    manual_override BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create chaos test results table
CREATE TABLE IF NOT EXISTS lte.chaos_test_results (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    test_type VARCHAR(100) NOT NULL, -- 'container_kill', 'cpu_stress', 'db_outage'
    test_duration_ms INTEGER NOT NULL,
    recovery_time_ms INTEGER,
    recovery_success BOOLEAN NOT NULL,
    slo_violation BOOLEAN DEFAULT FALSE,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create SLO definitions table
CREATE TABLE IF NOT EXISTS lte.slo_definitions (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    slo_target DECIMAL(10,6) NOT NULL,
    error_budget_percentage DECIMAL(5,2) NOT NULL, -- e.g., 0.1 for 0.1%
    window_days INTEGER NOT NULL DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(service_name, metric_type)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_error_budget_metrics_timestamp ON lte.error_budget_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_error_budget_metrics_service ON lte.error_budget_metrics(service_name);
CREATE INDEX IF NOT EXISTS idx_error_budget_metrics_window ON lte.error_budget_metrics(window_start, window_end);

CREATE INDEX IF NOT EXISTS idx_recovery_actions_timestamp ON lte.recovery_actions(timestamp);
CREATE INDEX IF NOT EXISTS idx_recovery_actions_service ON lte.recovery_actions(service_name);
CREATE INDEX IF NOT EXISTS idx_recovery_actions_type ON lte.recovery_actions(action_type);

CREATE INDEX IF NOT EXISTS idx_chaos_test_results_timestamp ON lte.chaos_test_results(timestamp);
CREATE INDEX IF NOT EXISTS idx_chaos_test_results_type ON lte.chaos_test_results(test_type);

-- Insert default SLO definitions
INSERT INTO lte.slo_definitions (service_name, metric_type, slo_target, error_budget_percentage, window_days) VALUES
    ('api', 'availability', 99.9, 0.1, 30),
    ('api', 'latency_p95', 1000.0, 0.1, 30), -- 1 second in milliseconds
    ('api', 'error_rate', 0.1, 0.1, 30),
    ('dashboard', 'availability', 99.9, 0.1, 30),
    ('dashboard', 'latency_p95', 2500.0, 0.1, 30), -- 2.5 seconds for UI
    ('database', 'availability', 99.99, 0.01, 30),
    ('database', 'latency_p95', 100.0, 0.1, 30) -- 100ms for DB queries
ON CONFLICT (service_name, metric_type) DO NOTHING;

-- Create function to calculate error budget consumption
CREATE OR REPLACE FUNCTION lte.calculate_error_budget_consumption(
    p_service_name VARCHAR(100),
    p_metric_type VARCHAR(50),
    p_window_days INTEGER DEFAULT 30
)
RETURNS TABLE(
    error_budget_consumed DECIMAL(10,6),
    error_budget_remaining DECIMAL(10,6),
    current_value DECIMAL(10,6),
    slo_target DECIMAL(10,6)
) AS $$
BEGIN
    RETURN QUERY
    WITH slo_def AS (
        SELECT slo_target, error_budget_percentage
        FROM lte.slo_definitions
        WHERE service_name = p_service_name 
        AND metric_type = p_metric_type 
        AND is_active = TRUE
    ),
    current_metrics AS (
        SELECT 
            AVG(metric_value) as current_value,
            MAX(slo_target) as slo_target
        FROM lte.error_budget_metrics ebm
        CROSS JOIN slo_def
        WHERE ebm.service_name = p_service_name 
        AND ebm.metric_type = p_metric_type
        AND ebm.timestamp >= NOW() - INTERVAL '1 day' * p_window_days
    )
    SELECT 
        CASE 
            WHEN cm.current_value IS NULL THEN 0.0
            WHEN p_metric_type = 'availability' THEN 
                GREATEST(0, (slo_def.slo_target - cm.current_value) / slo_def.slo_target * 100)
            WHEN p_metric_type = 'latency_p95' THEN 
                GREATEST(0, (cm.current_value - slo_def.slo_target) / slo_def.slo_target * 100)
            WHEN p_metric_type = 'error_rate' THEN 
                GREATEST(0, (cm.current_value - slo_def.slo_target) / slo_def.slo_target * 100)
            ELSE 0.0
        END as error_budget_consumed,
        GREATEST(0, slo_def.error_budget_percentage - 
            CASE 
                WHEN cm.current_value IS NULL THEN 0.0
                WHEN p_metric_type = 'availability' THEN 
                    GREATEST(0, (slo_def.slo_target - cm.current_value) / slo_def.slo_target * 100)
                WHEN p_metric_type = 'latency_p95' THEN 
                    GREATEST(0, (cm.current_value - slo_def.slo_target) / slo_def.slo_target * 100)
                WHEN p_metric_type = 'error_rate' THEN 
                    GREATEST(0, (cm.current_value - slo_def.slo_target) / slo_def.slo_target * 100)
                ELSE 0.0
            END
        ) as error_budget_remaining,
        COALESCE(cm.current_value, 0.0) as current_value,
        COALESCE(cm.slo_target, 0.0) as slo_target
    FROM slo_def
    CROSS JOIN current_metrics cm;
END;
$$ LANGUAGE plpgsql;

-- Create function to record error budget metrics
CREATE OR REPLACE FUNCTION lte.record_error_budget_metric(
    p_service_name VARCHAR(100),
    p_metric_type VARCHAR(50),
    p_metric_value DECIMAL(10,6)
)
RETURNS INTEGER AS $$
DECLARE
    v_slo_target DECIMAL(10,6);
    v_error_budget_consumed DECIMAL(10,6);
    v_error_budget_remaining DECIMAL(10,6);
    v_window_start TIMESTAMP WITH TIME ZONE;
    v_window_end TIMESTAMP WITH TIME ZONE;
    v_inserted_id INTEGER;
BEGIN
    -- Get SLO target
    SELECT slo_target INTO v_slo_target
    FROM lte.slo_definitions
    WHERE service_name = p_service_name 
    AND metric_type = p_metric_type 
    AND is_active = TRUE;
    
    IF v_slo_target IS NULL THEN
        RAISE EXCEPTION 'No SLO definition found for service % and metric type %', p_service_name, p_metric_type;
    END IF;
    
    -- Calculate error budget consumption
    SELECT 
        error_budget_consumed,
        error_budget_remaining
    INTO v_error_budget_consumed, v_error_budget_remaining
    FROM lte.calculate_error_budget_consumption(p_service_name, p_metric_type);
    
    -- Set window (30-day rolling window)
    v_window_start := NOW() - INTERVAL '30 days';
    v_window_end := NOW();
    
    -- Insert metric record
    INSERT INTO lte.error_budget_metrics (
        service_name, metric_type, metric_value, slo_target,
        error_budget_consumed, error_budget_remaining,
        window_start, window_end
    ) VALUES (
        p_service_name, p_metric_type, p_metric_value, v_slo_target,
        v_error_budget_consumed, v_error_budget_remaining,
        v_window_start, v_window_end
    ) RETURNING id INTO v_inserted_id;
    
    RETURN v_inserted_id;
END;
$$ LANGUAGE plpgsql;

-- Create function to record recovery action
CREATE OR REPLACE FUNCTION lte.record_recovery_action(
    p_action_type VARCHAR(100),
    p_service_name VARCHAR(100),
    p_trigger_reason TEXT,
    p_success BOOLEAN,
    p_duration_ms INTEGER DEFAULT NULL,
    p_error_message TEXT DEFAULT NULL,
    p_manual_override BOOLEAN DEFAULT FALSE
)
RETURNS INTEGER AS $$
DECLARE
    v_inserted_id INTEGER;
BEGIN
    INSERT INTO lte.recovery_actions (
        action_type, service_name, trigger_reason, success,
        duration_ms, error_message, manual_override
    ) VALUES (
        p_action_type, p_service_name, p_trigger_reason, p_success,
        p_duration_ms, p_error_message, p_manual_override
    ) RETURNING id INTO v_inserted_id;
    
    RETURN v_inserted_id;
END;
$$ LANGUAGE plpgsql;

-- Create function to record chaos test result
CREATE OR REPLACE FUNCTION lte.record_chaos_test_result(
    p_test_type VARCHAR(100),
    p_test_duration_ms INTEGER,
    p_recovery_time_ms INTEGER DEFAULT NULL,
    p_recovery_success BOOLEAN DEFAULT FALSE,
    p_slo_violation BOOLEAN DEFAULT FALSE,
    p_details JSONB DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_inserted_id INTEGER;
BEGIN
    INSERT INTO lte.chaos_test_results (
        test_type, test_duration_ms, recovery_time_ms,
        recovery_success, slo_violation, details
    ) VALUES (
        p_test_type, p_test_duration_ms, p_recovery_time_ms,
        p_recovery_success, p_slo_violation, p_details
    ) RETURNING id INTO v_inserted_id;
    
    RETURN v_inserted_id;
END;
$$ LANGUAGE plpgsql;
