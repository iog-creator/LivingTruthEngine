-- Resilience & Predictive Monitoring Schema
-- Phase 9.5.6 - Chaos Engineering & Proactive Resilience

-- Create anomaly detection table
CREATE TABLE IF NOT EXISTS lte.anomaly_detections (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    service_name VARCHAR(100) NOT NULL,
    metric_type VARCHAR(50) NOT NULL, -- 'latency', 'error_rate', 'memory_usage', 'queue_depth'
    metric_value DECIMAL(10,6) NOT NULL,
    baseline_value DECIMAL(10,6) NOT NULL,
    deviation_percentage DECIMAL(10,6) NOT NULL,
    severity VARCHAR(20) NOT NULL, -- 'low', 'medium', 'high', 'critical'
    anomaly_type VARCHAR(50) NOT NULL, -- 'spike', 'trend', 'seasonal', 'threshold'
    predicted_impact TEXT,
    alert_sent BOOLEAN DEFAULT FALSE,
    alert_sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create predictive models table
CREATE TABLE IF NOT EXISTS lte.predictive_models (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    service_name VARCHAR(100) NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    model_type VARCHAR(50) NOT NULL, -- 'rolling_average', 'linear_regression', 'ml_model'
    model_config JSONB NOT NULL,
    accuracy_score DECIMAL(5,4),
    last_trained TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(model_name, service_name, metric_type)
);

-- Create predictions table
CREATE TABLE IF NOT EXISTS lte.predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    model_id INTEGER REFERENCES lte.predictive_models(id),
    service_name VARCHAR(100) NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    predicted_value DECIMAL(10,6) NOT NULL,
    confidence_interval_lower DECIMAL(10,6),
    confidence_interval_upper DECIMAL(10,6),
    prediction_horizon_minutes INTEGER NOT NULL, -- how far ahead this prediction is
    actual_value DECIMAL(10,6), -- filled in when actual value is known
    accuracy DECIMAL(5,4), -- how accurate the prediction was
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create proactive recovery actions table
CREATE TABLE IF NOT EXISTS lte.proactive_recovery_actions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    action_type VARCHAR(100) NOT NULL, -- 'scale_up', 'graceful_degradation', 'preemptive_restart'
    service_name VARCHAR(100) NOT NULL,
    trigger_reason TEXT NOT NULL,
    predicted_stress_level VARCHAR(20) NOT NULL, -- 'low', 'medium', 'high', 'critical'
    action_parameters JSONB,
    success BOOLEAN NOT NULL,
    duration_ms INTEGER,
    impact_mitigated BOOLEAN DEFAULT FALSE,
    manual_override BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create resilience scores table
CREATE TABLE IF NOT EXISTS lte.resilience_scores (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    overall_score DECIMAL(5,2) NOT NULL, -- 0-100 scale
    chaos_test_score DECIMAL(5,2) NOT NULL,
    recovery_score DECIMAL(5,2) NOT NULL,
    prediction_score DECIMAL(5,2) NOT NULL,
    anomaly_score DECIMAL(5,2) NOT NULL,
    test_count INTEGER NOT NULL,
    recent_failures INTEGER NOT NULL,
    recovery_time_avg_ms INTEGER,
    prediction_accuracy_avg DECIMAL(5,4),
    score_components JSONB, -- detailed breakdown of score calculation
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create enhanced chaos scenarios table
CREATE TABLE IF NOT EXISTS lte.chaos_scenarios (
    id SERIAL PRIMARY KEY,
    scenario_name VARCHAR(100) NOT NULL,
    scenario_type VARCHAR(50) NOT NULL, -- 'service_kill', 'network_latency', 'db_exhaustion', 'cpu_pressure', 'queue_failure'
    blast_radius VARCHAR(20) NOT NULL, -- 'small', 'medium', 'large'
    duration_seconds INTEGER NOT NULL,
    parameters JSONB, -- scenario-specific parameters
    safeguards JSONB, -- safety limits and rollback conditions
    is_scheduled BOOLEAN DEFAULT FALSE,
    schedule_cron VARCHAR(100), -- cron expression for scheduled runs
    last_run TIMESTAMP WITH TIME ZONE,
    next_run TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create chaos scenario results table
CREATE TABLE IF NOT EXISTS lte.chaos_scenario_results (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    scenario_id INTEGER REFERENCES lte.chaos_scenarios(id),
    scenario_name VARCHAR(100) NOT NULL,
    scenario_type VARCHAR(50) NOT NULL,
    blast_radius VARCHAR(20) NOT NULL,
    duration_seconds INTEGER NOT NULL,
    test_duration_ms INTEGER NOT NULL,
    recovery_time_ms INTEGER,
    recovery_success BOOLEAN NOT NULL,
    slo_violation BOOLEAN DEFAULT FALSE,
    impact_metrics JSONB, -- detailed impact measurements
    recovery_actions JSONB, -- actions taken during recovery
    resilience_score_impact DECIMAL(5,2), -- how this test affected resilience score
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_anomaly_detections_timestamp ON lte.anomaly_detections(timestamp);
CREATE INDEX IF NOT EXISTS idx_anomaly_detections_service ON lte.anomaly_detections(service_name);
CREATE INDEX IF NOT EXISTS idx_anomaly_detections_severity ON lte.anomaly_detections(severity);

CREATE INDEX IF NOT EXISTS idx_predictions_timestamp ON lte.predictions(timestamp);
CREATE INDEX IF NOT EXISTS idx_predictions_service ON lte.predictions(service_name);
CREATE INDEX IF NOT EXISTS idx_predictions_model ON lte.predictions(model_id);

CREATE INDEX IF NOT EXISTS idx_proactive_recovery_timestamp ON lte.proactive_recovery_actions(timestamp);
CREATE INDEX IF NOT EXISTS idx_proactive_recovery_service ON lte.proactive_recovery_actions(service_name);
CREATE INDEX IF NOT EXISTS idx_proactive_recovery_type ON lte.proactive_recovery_actions(action_type);

CREATE INDEX IF NOT EXISTS idx_resilience_scores_timestamp ON lte.resilience_scores(timestamp);
CREATE INDEX IF NOT EXISTS idx_resilience_scores_overall ON lte.resilience_scores(overall_score);

CREATE INDEX IF NOT EXISTS idx_chaos_scenarios_type ON lte.chaos_scenarios(scenario_type);
CREATE INDEX IF NOT EXISTS idx_chaos_scenarios_scheduled ON lte.chaos_scenarios(is_scheduled, next_run);

CREATE INDEX IF NOT EXISTS idx_chaos_scenario_results_timestamp ON lte.chaos_scenario_results(timestamp);
CREATE INDEX IF NOT EXISTS idx_chaos_scenario_results_scenario ON lte.chaos_scenario_results(scenario_id);

-- Insert default chaos scenarios
INSERT INTO lte.chaos_scenarios (scenario_name, scenario_type, blast_radius, duration_seconds, parameters, safeguards) VALUES
    ('dashboard_service_kill', 'service_kill', 'small', 30, '{"service": "dashboard", "kill_method": "docker_kill"}', '{"max_downtime_seconds": 60, "auto_restart": true}'),
    ('network_latency_injection', 'network_latency', 'medium', 60, '{"latency_ms": 100, "packet_loss_percent": 5}', '{"max_latency_ms": 500, "auto_cleanup": true}'),
    ('db_connection_exhaustion', 'db_exhaustion', 'medium', 45, '{"max_connections": 5, "connection_timeout_ms": 5000}', '{"max_downtime_seconds": 120, "connection_pool_reset": true}'),
    ('cpu_pressure_test', 'cpu_pressure', 'small', 90, '{"cpu_cores": 2, "load_percentage": 80}', '{"max_cpu_percentage": 95, "auto_throttle": true}'),
    ('memory_pressure_test', 'memory_pressure', 'medium', 60, '{"memory_gb": 1, "pressure_duration_seconds": 30}', '{"max_memory_percentage": 90, "auto_cleanup": true}'),
    ('queue_delay_simulation', 'queue_failure', 'small', 30, '{"delay_seconds": 10, "queue_size_limit": 100}', '{"max_delay_seconds": 60, "queue_overflow_protection": true}')
ON CONFLICT DO NOTHING;

-- Create function to calculate resilience score
CREATE OR REPLACE FUNCTION lte.calculate_resilience_score(
    p_window_hours INTEGER DEFAULT 24
)
RETURNS TABLE(
    overall_score DECIMAL(5,2),
    chaos_test_score DECIMAL(5,2),
    recovery_score DECIMAL(5,2),
    prediction_score DECIMAL(5,2),
    anomaly_score DECIMAL(5,2),
    test_count INTEGER,
    recent_failures INTEGER,
    recovery_time_avg_ms INTEGER,
    prediction_accuracy_avg DECIMAL(5,4)
) AS $$
BEGIN
    RETURN QUERY
    WITH chaos_stats AS (
        SELECT 
            COUNT(*) as test_count,
            COUNT(*) FILTER (WHERE recovery_success = FALSE) as failures,
            AVG(recovery_time_ms) FILTER (WHERE recovery_success = TRUE) as avg_recovery_time,
            CASE 
                WHEN COUNT(*) = 0 THEN 100.0
                ELSE (COUNT(*) FILTER (WHERE recovery_success = TRUE)::DECIMAL / COUNT(*)::DECIMAL) * 100
            END as chaos_score
        FROM lte.chaos_scenario_results
        WHERE timestamp >= NOW() - INTERVAL '1 hour' * p_window_hours
    ),
    recovery_stats AS (
        SELECT 
            COUNT(*) as action_count,
            AVG(duration_ms) FILTER (WHERE success = TRUE) as avg_recovery_duration,
            CASE 
                WHEN COUNT(*) = 0 THEN 100.0
                ELSE (COUNT(*) FILTER (WHERE success = TRUE)::DECIMAL / COUNT(*)::DECIMAL) * 100
            END as recovery_score
        FROM lte.proactive_recovery_actions
        WHERE timestamp >= NOW() - INTERVAL '1 hour' * p_window_hours
    ),
    prediction_stats AS (
        SELECT 
            COUNT(*) as prediction_count,
            AVG(accuracy) FILTER (WHERE accuracy IS NOT NULL) as avg_accuracy,
            CASE 
                WHEN COUNT(*) = 0 THEN 100.0
                ELSE COALESCE(AVG(accuracy) FILTER (WHERE accuracy IS NOT NULL), 100.0) * 100
            END as prediction_score
        FROM lte.predictions
        WHERE timestamp >= NOW() - INTERVAL '1 hour' * p_window_hours
    ),
    anomaly_stats AS (
        SELECT 
            COUNT(*) as anomaly_count,
            CASE 
                WHEN COUNT(*) = 0 THEN 100.0
                ELSE GREATEST(0, 100 - (COUNT(*) * 5)) -- 5 points per anomaly
            END as anomaly_score
        FROM lte.anomaly_detections
        WHERE timestamp >= NOW() - INTERVAL '1 hour' * p_window_hours
        AND severity IN ('high', 'critical')
    )
    SELECT 
        (cs.chaos_score * 0.3 + rs.recovery_score * 0.3 + ps.prediction_score * 0.2 + ans.anomaly_score * 0.2) as overall_score,
        cs.chaos_score,
        rs.recovery_score,
        ps.prediction_score,
        ans.anomaly_score,
        cs.test_count,
        cs.failures,
        cs.avg_recovery_time::INTEGER,
        ps.avg_accuracy
    FROM chaos_stats cs
    CROSS JOIN recovery_stats rs
    CROSS JOIN prediction_stats ps
    CROSS JOIN anomaly_stats ans;
END;
$$ LANGUAGE plpgsql;

-- Create function to record anomaly detection
CREATE OR REPLACE FUNCTION lte.record_anomaly_detection(
    p_service_name VARCHAR(100),
    p_metric_type VARCHAR(50),
    p_metric_value DECIMAL(10,6),
    p_baseline_value DECIMAL(10,6),
    p_deviation_percentage DECIMAL(10,6),
    p_severity VARCHAR(20),
    p_anomaly_type VARCHAR(50),
    p_predicted_impact TEXT DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_inserted_id INTEGER;
BEGIN
    INSERT INTO lte.anomaly_detections (
        service_name, metric_type, metric_value, baseline_value,
        deviation_percentage, severity, anomaly_type, predicted_impact
    ) VALUES (
        p_service_name, p_metric_type, p_metric_value, p_baseline_value,
        p_deviation_percentage, p_severity, p_anomaly_type, p_predicted_impact
    ) RETURNING id INTO v_inserted_id;
    
    RETURN v_inserted_id;
END;
$$ LANGUAGE plpgsql;

-- Create function to record prediction
CREATE OR REPLACE FUNCTION lte.record_prediction(
    p_model_id INTEGER,
    p_service_name VARCHAR(100),
    p_metric_type VARCHAR(50),
    p_predicted_value DECIMAL(10,6),
    p_confidence_interval_lower DECIMAL(10,6) DEFAULT NULL,
    p_confidence_interval_upper DECIMAL(10,6) DEFAULT NULL,
    p_prediction_horizon_minutes INTEGER DEFAULT 5
)
RETURNS INTEGER AS $$
DECLARE
    v_inserted_id INTEGER;
BEGIN
    INSERT INTO lte.predictions (
        model_id, service_name, metric_type, predicted_value,
        confidence_interval_lower, confidence_interval_upper, prediction_horizon_minutes
    ) VALUES (
        p_model_id, p_service_name, p_metric_type, p_predicted_value,
        p_confidence_interval_lower, p_confidence_interval_upper, p_prediction_horizon_minutes
    ) RETURNING id INTO v_inserted_id;
    
    RETURN v_inserted_id;
END;
$$ LANGUAGE plpgsql;

-- Create function to record proactive recovery action
CREATE OR REPLACE FUNCTION lte.record_proactive_recovery_action(
    p_action_type VARCHAR(100),
    p_service_name VARCHAR(100),
    p_trigger_reason TEXT,
    p_predicted_stress_level VARCHAR(20),
    p_action_parameters JSONB DEFAULT NULL,
    p_success BOOLEAN,
    p_duration_ms INTEGER DEFAULT NULL,
    p_impact_mitigated BOOLEAN DEFAULT FALSE,
    p_manual_override BOOLEAN DEFAULT FALSE
)
RETURNS INTEGER AS $$
DECLARE
    v_inserted_id INTEGER;
BEGIN
    INSERT INTO lte.proactive_recovery_actions (
        action_type, service_name, trigger_reason, predicted_stress_level,
        action_parameters, success, duration_ms, impact_mitigated, manual_override
    ) VALUES (
        p_action_type, p_service_name, p_trigger_reason, p_predicted_stress_level,
        p_action_parameters, p_success, p_duration_ms, p_impact_mitigated, p_manual_override
    ) RETURNING id INTO v_inserted_id;
    
    RETURN v_inserted_id;
END;
$$ LANGUAGE plpgsql;

-- Create function to record chaos scenario result
CREATE OR REPLACE FUNCTION lte.record_chaos_scenario_result(
    p_scenario_id INTEGER,
    p_scenario_name VARCHAR(100),
    p_scenario_type VARCHAR(50),
    p_blast_radius VARCHAR(20),
    p_duration_seconds INTEGER,
    p_test_duration_ms INTEGER,
    p_recovery_time_ms INTEGER DEFAULT NULL,
    p_recovery_success BOOLEAN,
    p_slo_violation BOOLEAN DEFAULT FALSE,
    p_impact_metrics JSONB DEFAULT NULL,
    p_recovery_actions JSONB DEFAULT NULL,
    p_resilience_score_impact DECIMAL(5,2) DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_inserted_id INTEGER;
BEGIN
    INSERT INTO lte.chaos_scenario_results (
        scenario_id, scenario_name, scenario_type, blast_radius, duration_seconds,
        test_duration_ms, recovery_time_ms, recovery_success, slo_violation,
        impact_metrics, recovery_actions, resilience_score_impact
    ) VALUES (
        p_scenario_id, p_scenario_name, p_scenario_type, p_blast_radius, p_duration_seconds,
        p_test_duration_ms, p_recovery_time_ms, p_recovery_success, p_slo_violation,
        p_impact_metrics, p_recovery_actions, p_resilience_score_impact
    ) RETURNING id INTO v_inserted_id;
    
    RETURN v_inserted_id;
END;
$$ LANGUAGE plpgsql;

-- Create function to update resilience score
CREATE OR REPLACE FUNCTION lte.update_resilience_score()
RETURNS INTEGER AS $$
DECLARE
    v_inserted_id INTEGER;
    v_score_record RECORD;
BEGIN
    -- Calculate current resilience score
    SELECT * INTO v_score_record
    FROM lte.calculate_resilience_score(24);
    
    -- Insert the score
    INSERT INTO lte.resilience_scores (
        overall_score, chaos_test_score, recovery_score, prediction_score, anomaly_score,
        test_count, recent_failures, recovery_time_avg_ms, prediction_accuracy_avg,
        score_components
    ) VALUES (
        v_score_record.overall_score, v_score_record.chaos_test_score, v_score_record.recovery_score,
        v_score_record.prediction_score, v_score_record.anomaly_score, v_score_record.test_count,
        v_score_record.recent_failures, v_score_record.recovery_time_avg_ms, v_score_record.prediction_accuracy_avg,
        jsonb_build_object(
            'chaos_weight', 0.3,
            'recovery_weight', 0.3,
            'prediction_weight', 0.2,
            'anomaly_weight', 0.2
        )
    ) RETURNING id INTO v_inserted_id;
    
    RETURN v_inserted_id;
END;
$$ LANGUAGE plpgsql;
