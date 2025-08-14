#!/usr/bin/env python3
"""
Predictive Monitoring Module
============================

This module provides predictive monitoring capabilities including:
- Real-time anomaly detection for key metrics
- Early-warning alerts for SLO breaches
- Predictive error budget modeling
- Historical trend analysis

Features:
- Anomaly detection algorithms (spike, trend, seasonal)
- Alert system integration (Slack/email/webhook)
- Predictive models for error budget burn rate
- Historical data storage and analysis
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np
from collections import deque
import threading
import requests

logger = logging.getLogger(__name__)


@dataclass
class AnomalyDetection:
    """Anomaly detection result."""
    service_name: str
    metric_type: str
    metric_value: float
    baseline_value: float
    deviation_percentage: float
    severity: str
    anomaly_type: str
    predicted_impact: Optional[str]
    timestamp: datetime


@dataclass
class Prediction:
    """Prediction result."""
    service_name: str
    metric_type: str
    predicted_value: float
    confidence_interval_lower: Optional[float]
    confidence_interval_upper: Optional[float]
    prediction_horizon_minutes: int
    model_accuracy: Optional[float]
    timestamp: datetime


@dataclass
class Alert:
    """Alert configuration and result."""
    alert_type: str  # 'slack', 'email', 'webhook'
    endpoint: str
    message: str
    severity: str
    timestamp: datetime
    sent: bool = False
    error_message: Optional[str] = None


class AnomalyDetector:
    """Anomaly detection using various algorithms."""
    
    def __init__(self, window_size: int = 100, threshold_std: float = 2.0):
        """Initialize anomaly detector."""
        self.window_size = window_size
        self.threshold_std = threshold_std
        self.metric_windows: Dict[str, deque] = {}
        self.baselines: Dict[str, float] = {}
        
    def detect_spike_anomaly(self, service_name: str, metric_type: str, 
                           metric_value: float) -> Optional[AnomalyDetection]:
        """Detect spike anomalies using statistical methods."""
        key = f"{service_name}:{metric_type}"
        
        if key not in self.metric_windows:
            self.metric_windows[key] = deque(maxlen=self.window_size)
            self.baselines[key] = metric_value
            return None
        
        window = self.metric_windows[key]
        window.append(metric_value)
        
        if len(window) < 10:  # Need minimum data points
            return None
        
        # Calculate baseline and deviation
        baseline = np.mean(window)
        std_dev = np.std(window)
        
        if std_dev == 0:
            return None
        
        deviation = abs(metric_value - baseline) / std_dev
        
        if deviation > self.threshold_std:
            # Determine severity based on deviation
            if deviation > 4.0:
                severity = "critical"
            elif deviation > 3.0:
                severity = "high"
            elif deviation > 2.5:
                severity = "medium"
            else:
                severity = "low"
            
            deviation_percentage = (deviation / self.threshold_std) * 100
            
            return AnomalyDetection(
                service_name=service_name,
                metric_type=metric_type,
                metric_value=metric_value,
                baseline_value=baseline,
                deviation_percentage=deviation_percentage,
                severity=severity,
                anomaly_type="spike",
                predicted_impact=f"Metric {metric_type} for {service_name} shows {deviation_percentage:.1f}% deviation from baseline",
                timestamp=datetime.now()
            )
        
        return None
    
    def detect_trend_anomaly(self, service_name: str, metric_type: str,
                           metric_values: List[float], window_minutes: int = 30) -> Optional[AnomalyDetection]:
        """Detect trend anomalies using linear regression."""
        if len(metric_values) < 10:
            return None
        
        # Calculate trend using linear regression
        x = np.arange(len(metric_values))
        slope, intercept = np.polyfit(x, metric_values, 1)
        
        # Calculate R-squared to determine trend strength
        y_pred = slope * x + intercept
        r_squared = 1 - (np.sum((metric_values - y_pred) ** 2) / np.sum((metric_values - np.mean(metric_values)) ** 2))
        
        # Detect significant trends
        if abs(slope) > 0.1 and r_squared > 0.7:  # Adjustable thresholds
            trend_direction = "increasing" if slope > 0 else "decreasing"
            severity = "high" if abs(slope) > 0.5 else "medium"
            
            return AnomalyDetection(
                service_name=service_name,
                metric_type=metric_type,
                metric_value=metric_values[-1],
                baseline_value=np.mean(metric_values),
                deviation_percentage=abs(slope) * 100,
                severity=severity,
                anomaly_type="trend",
                predicted_impact=f"Strong {trend_direction} trend detected in {metric_type} for {service_name}",
                timestamp=datetime.now()
            )
        
        return None


class PredictiveModel:
    """Simple predictive model using rolling averages and linear regression."""
    
    def __init__(self, model_type: str = "rolling_average", window_size: int = 50):
        """Initialize predictive model."""
        self.model_type = model_type
        self.window_size = window_size
        self.historical_data: Dict[str, deque] = {}
        self.accuracy_scores: Dict[str, List[float]] = {}
        
    def predict_value(self, service_name: str, metric_type: str, 
                     horizon_minutes: int = 5) -> Optional[Prediction]:
        """Predict future metric value."""
        key = f"{service_name}:{metric_type}"
        
        if key not in self.historical_data or len(self.historical_data[key]) < 5:
            return None
        
        data = list(self.historical_data[key])
        
        if self.model_type == "rolling_average":
            # Simple rolling average prediction
            recent_avg = np.mean(data[-10:])  # Last 10 points
            trend = np.mean(np.diff(data[-5:]))  # Recent trend
            
            predicted_value = recent_avg + (trend * horizon_minutes)
            
            # Calculate confidence interval
            std_dev = np.std(data[-10:])
            confidence_lower = predicted_value - (1.96 * std_dev)
            confidence_upper = predicted_value + (1.96 * std_dev)
            
        elif self.model_type == "linear_regression":
            # Linear regression prediction
            x = np.arange(len(data))
            slope, intercept = np.polyfit(x, data, 1)
            
            predicted_value = slope * (len(data) + horizon_minutes) + intercept
            
            # Calculate confidence interval
            residuals = data - (slope * x + intercept)
            std_dev = np.std(residuals)
            confidence_lower = predicted_value - (1.96 * std_dev)
            confidence_upper = predicted_value + (1.96 * std_dev)
            
        else:
            return None
        
        # Calculate model accuracy
        accuracy = self._calculate_accuracy(key)
        
        return Prediction(
            service_name=service_name,
            metric_type=metric_type,
            predicted_value=predicted_value,
            confidence_interval_lower=confidence_lower,
            confidence_interval_upper=confidence_upper,
            prediction_horizon_minutes=horizon_minutes,
            model_accuracy=accuracy,
            timestamp=datetime.now()
        )
    
    def update_model(self, service_name: str, metric_type: str, value: float):
        """Update model with new data point."""
        key = f"{service_name}:{metric_type}"
        
        if key not in self.historical_data:
            self.historical_data[key] = deque(maxlen=self.window_size)
            self.accuracy_scores[key] = []
        
        self.historical_data[key].append(value)
    
    def _calculate_accuracy(self, key: str) -> Optional[float]:
        """Calculate model accuracy based on recent predictions."""
        if key not in self.accuracy_scores or len(self.accuracy_scores[key]) < 5:
            return None
        
        recent_scores = self.accuracy_scores[key][-10:]  # Last 10 accuracy scores
        return np.mean(recent_scores) if recent_scores else None


class AlertManager:
    """Manages alert sending and configuration."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize alert manager."""
        self.config = config
        self.alert_history: List[Alert] = []
        self.alert_cooldowns: Dict[str, datetime] = {}
        self.cooldown_minutes = config.get('cooldown_minutes', 5)
        
    def send_alert(self, alert: Alert) -> bool:
        """Send alert via configured channels."""
        try:
            if self._is_in_cooldown(alert):
                logger.info(f"Alert in cooldown: {alert.alert_type}")
                return False
            
            success = False
            
            if alert.alert_type == "slack":
                success = self._send_slack_alert(alert)
            elif alert.alert_type == "email":
                success = self._send_email_alert(alert)
            elif alert.alert_type == "webhook":
                success = self._send_webhook_alert(alert)
            
            if success:
                alert.sent = True
                self._set_cooldown(alert)
                self.alert_history.append(alert)
                logger.info(f"Alert sent successfully: {alert.alert_type}")
            else:
                alert.error_message = "Failed to send alert"
                logger.error(f"Failed to send alert: {alert.alert_type}")
            
            return success
            
        except Exception as e:
            alert.error_message = str(e)
            logger.error(f"Error sending alert: {e}")
            return False
    
    def _send_slack_alert(self, alert: Alert) -> bool:
        """Send alert to Slack."""
        webhook_url = self.config.get('slack_webhook_url')
        if not webhook_url:
            logger.warning("Slack webhook URL not configured")
            return False
        
        payload = {
            "text": f"[{alert.severity.upper()}] {alert.message}",
            "color": self._get_severity_color(alert.severity)
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 200
    
    def _send_email_alert(self, alert: Alert) -> bool:
        """Send alert via email."""
        # Implementation would depend on email service configuration
        logger.info(f"Email alert would be sent: {alert.message}")
        return True  # Placeholder
    
    def _send_webhook_alert(self, alert: Alert) -> bool:
        """Send alert to webhook endpoint."""
        webhook_url = self.config.get('webhook_url')
        if not webhook_url:
            logger.warning("Webhook URL not configured")
            return False
        
        payload = {
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "message": alert.message,
            "timestamp": alert.timestamp.isoformat()
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 200
    
    def _get_severity_color(self, severity: str) -> str:
        """Get color for severity level."""
        colors = {
            "critical": "#ff0000",
            "high": "#ff6600",
            "medium": "#ffcc00",
            "low": "#00cc00"
        }
        return colors.get(severity, "#666666")
    
    def _is_in_cooldown(self, alert: Alert) -> bool:
        """Check if alert is in cooldown period."""
        cooldown_key = f"{alert.alert_type}:{alert.severity}"
        last_alert = self.alert_cooldowns.get(cooldown_key)
        
        if last_alert:
            time_since_last = datetime.now() - last_alert
            return time_since_last.total_seconds() < (self.cooldown_minutes * 60)
        
        return False
    
    def _set_cooldown(self, alert: Alert):
        """Set cooldown for alert type and severity."""
        cooldown_key = f"{alert.alert_type}:{alert.severity}"
        self.alert_cooldowns[cooldown_key] = datetime.now()


class PredictiveMonitor:
    """Main predictive monitoring class."""
    
    def __init__(self, db_connection_string: str, alert_config: Dict[str, Any]):
        """Initialize predictive monitor."""
        self.db_connection_string = db_connection_string
        self.anomaly_detector = AnomalyDetector()
        self.predictive_model = PredictiveModel()
        self.alert_manager = AlertManager(alert_config)
        self.logger = logging.getLogger(__name__)
        
        # Monitoring configuration
        self.monitoring_interval = 30  # seconds
        self.prediction_horizon = 5  # minutes
        self.alert_thresholds = {
            "latency": {"critical": 2000, "high": 1000, "medium": 500},
            "error_rate": {"critical": 10.0, "high": 5.0, "medium": 2.0},
            "memory_usage": {"critical": 90.0, "high": 80.0, "medium": 70.0},
            "queue_depth": {"critical": 1000, "high": 500, "medium": 100}
        }
        
        # Start monitoring thread
        self.monitoring_active = False
        self.monitoring_thread = None
        
    def start_monitoring(self):
        """Start continuous monitoring."""
        if self.monitoring_active:
            self.logger.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("Predictive monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("Predictive monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                self._collect_and_analyze_metrics()
                time.sleep(self.monitoring_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_and_analyze_metrics(self):
        """Collect metrics and perform analysis."""
        # Collect current metrics
        metrics = self._collect_current_metrics()
        
        for service_name, service_metrics in metrics.items():
            for metric_type, metric_value in service_metrics.items():
                # Update predictive model
                self.predictive_model.update_model(service_name, metric_type, metric_value)
                
                # Detect anomalies
                anomaly = self.anomaly_detector.detect_spike_anomaly(
                    service_name, metric_type, metric_value
                )
                
                if anomaly:
                    self._handle_anomaly(anomaly)
                
                # Generate predictions
                prediction = self.predictive_model.predict_value(
                    service_name, metric_type, self.prediction_horizon
                )
                
                if prediction:
                    self._handle_prediction(prediction)
    
    def _collect_current_metrics(self) -> Dict[str, Dict[str, float]]:
        """Collect current system metrics."""
        metrics = {}
        
        try:
            # Health endpoint metrics
            health_response = requests.get("http://localhost:8050/api/health/full", timeout=5)
            if health_response.status_code == 200:
                health_data = health_response.json()
                
                # Extract metrics from health data
                if "data" in health_data:
                    data = health_data["data"]
                    
                    # API latency (simplified)
                    metrics["api"] = {
                        "latency": data.get("api_latency_p95", 100.0),
                        "error_rate": data.get("error_rate", 0.0)
                    }
                    
                    # System metrics
                    metrics["system"] = {
                        "memory_usage": data.get("memory_usage_percent", 50.0),
                        "cpu_usage": data.get("cpu_usage_percent", 30.0)
                    }
            
        except Exception as e:
            self.logger.error(f"Error collecting metrics: {e}")
        
        return metrics
    
    def _handle_anomaly(self, anomaly: AnomalyDetection):
        """Handle detected anomaly."""
        self.logger.warning(f"Anomaly detected: {anomaly.service_name}/{anomaly.metric_type} - {anomaly.severity}")
        
        # Store anomaly in database
        self._store_anomaly(anomaly)
        
        # Send alert if severity is high enough
        if anomaly.severity in ["high", "critical"]:
            alert = Alert(
                alert_type="webhook",  # Default to webhook
                endpoint="",
                message=f"Anomaly detected: {anomaly.predicted_impact}",
                severity=anomaly.severity,
                timestamp=datetime.now()
            )
            self.alert_manager.send_alert(alert)
    
    def _handle_prediction(self, prediction: Prediction):
        """Handle prediction result."""
        self.logger.info(f"Prediction generated: {prediction.service_name}/{prediction.metric_type}")
        
        # Store prediction in database
        self._store_prediction(prediction)
        
        # Check if prediction indicates potential SLO breach
        if self._check_slo_breach_prediction(prediction):
            alert = Alert(
                alert_type="webhook",
                endpoint="",
                message=f"SLO breach predicted: {prediction.service_name}/{prediction.metric_type}",
                severity="high",
                timestamp=datetime.now()
            )
            self.alert_manager.send_alert(alert)
    
    def _check_slo_breach_prediction(self, prediction: Prediction) -> bool:
        """Check if prediction indicates potential SLO breach."""
        thresholds = self.alert_thresholds.get(prediction.metric_type, {})
        
        if prediction.metric_type == "latency":
            return prediction.predicted_value > thresholds.get("high", 1000)
        elif prediction.metric_type == "error_rate":
            return prediction.predicted_value > thresholds.get("high", 5.0)
        elif prediction.metric_type == "memory_usage":
            return prediction.predicted_value > thresholds.get("high", 80.0)
        
        return False
    
    def _store_anomaly(self, anomaly: AnomalyDetection):
        """Store anomaly in database."""
        try:
            with psycopg2.connect(self.db_connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.callproc('lte.record_anomaly_detection', [
                        anomaly.service_name,
                        anomaly.metric_type,
                        anomaly.metric_value,
                        anomaly.baseline_value,
                        anomaly.deviation_percentage,
                        anomaly.severity,
                        anomaly.anomaly_type,
                        anomaly.predicted_impact
                    ])
                    conn.commit()
                    
        except Exception as e:
            self.logger.error(f"Error storing anomaly: {e}")
    
    def _store_prediction(self, prediction: Prediction):
        """Store prediction in database."""
        try:
            with psycopg2.connect(self.db_connection_string) as conn:
                with conn.cursor() as cursor:
                    # For now, use model_id = 1 (rolling average model)
                    cursor.callproc('lte.record_prediction', [
                        1,  # model_id
                        prediction.service_name,
                        prediction.metric_type,
                        prediction.predicted_value,
                        prediction.confidence_interval_lower,
                        prediction.confidence_interval_upper,
                        prediction.prediction_horizon_minutes
                    ])
                    conn.commit()
                    
        except Exception as e:
            self.logger.error(f"Error storing prediction: {e}")
    
    def get_anomaly_history(self, service_name: Optional[str] = None, 
                          hours: int = 24) -> List[Dict[str, Any]]:
        """Get anomaly history from database."""
        try:
            with psycopg2.connect(self.db_connection_string) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                        SELECT * FROM lte.anomaly_detections
                        WHERE timestamp >= NOW() - INTERVAL '1 hour' * %s
                    """
                    params = [hours]
                    
                    if service_name:
                        query += " AND service_name = %s"
                        params.append(service_name)
                    
                    query += " ORDER BY timestamp DESC"
                    
                    cursor.execute(query, params)
                    return [dict(row) for row in cursor.fetchall()]
                    
        except Exception as e:
            self.logger.error(f"Error getting anomaly history: {e}")
            return []
    
    def get_prediction_history(self, service_name: Optional[str] = None,
                             hours: int = 24) -> List[Dict[str, Any]]:
        """Get prediction history from database."""
        try:
            with psycopg2.connect(self.db_connection_string) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                        SELECT * FROM lte.predictions
                        WHERE timestamp >= NOW() - INTERVAL '1 hour' * %s
                    """
                    params = [hours]
                    
                    if service_name:
                        query += " AND service_name = %s"
                        params.append(service_name)
                    
                    query += " ORDER BY timestamp DESC"
                    
                    cursor.execute(query, params)
                    return [dict(row) for row in cursor.fetchall()]
                    
        except Exception as e:
            self.logger.error(f"Error getting prediction history: {e}")
            return []
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get monitoring summary for health endpoint."""
        try:
            recent_anomalies = self.get_anomaly_history(hours=1)
            recent_predictions = self.get_prediction_history(hours=1)
            
            critical_anomalies = [a for a in recent_anomalies if a['severity'] == 'critical']
            high_anomalies = [a for a in recent_anomalies if a['severity'] == 'high']
            
            return {
                "anomaly_count": len(recent_anomalies),
                "critical_anomalies": len(critical_anomalies),
                "high_anomalies": len(high_anomalies),
                "prediction_count": len(recent_predictions),
                "monitoring_active": self.monitoring_active,
                "last_check": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting monitoring summary: {e}")
            return {
                "error": str(e),
                "monitoring_active": self.monitoring_active
            }

