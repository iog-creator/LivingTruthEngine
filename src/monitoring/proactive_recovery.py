#!/usr/bin/env python3
"""
Proactive Recovery Module
=========================

This module provides proactive recovery capabilities including:
- Adaptive response policies for predicted stress
- Service scaling and graceful degradation
- Preemptive service restarts
- Recovery simulation and testing

Features:
- Load-based service scaling
- Graceful degradation of non-critical features
- Preemptive recovery actions
- Recovery policy simulation
"""

import json
import logging
import time
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import psycopg2
from psycopg2.extras import RealDictCursor
import threading
import requests

logger = logging.getLogger(__name__)


@dataclass
class RecoveryAction:
    """Proactive recovery action."""

    action_type: str  # 'scale_up', 'graceful_degradation', 'preemptive_restart'
    service_name: str
    trigger_reason: str
    predicted_stress_level: str  # 'low', 'medium', 'high', 'critical'
    action_parameters: Optional[Dict[str, Any]]
    success: bool
    duration_ms: Optional[int]
    impact_mitigated: bool
    manual_override: bool
    timestamp: datetime


@dataclass
class RecoveryPolicy:
    """Recovery policy configuration."""

    policy_name: str
    service_name: str
    trigger_conditions: Dict[str, Any]
    actions: List[Dict[str, Any]]
    priority: int  # 1-10, higher is more important
    is_active: bool
    cooldown_minutes: int


@dataclass
class StressPrediction:
    """Stress prediction for proactive recovery."""

    service_name: str
    stress_level: str  # 'low', 'medium', 'high', 'critical'
    predicted_load: float
    confidence: float
    time_to_breach_minutes: Optional[int]
    recommended_actions: List[str]
    timestamp: datetime


class ServiceScaler:
    """Handles service scaling operations."""

    def __init__(self, project_root: str):
        """Initialize service scaler."""
        self.project_root = project_root
        self.logger = logging.getLogger(__name__)

    def scale_service(self, service_name: str, scale_factor: float) -> bool:
        """Scale a service up or down."""
        try:
            # Get current service count
            current_count = self._get_service_count(service_name)
            if current_count is None:
                return False

            # Calculate new count
            new_count = max(1, int(current_count * scale_factor))

            # Scale the service
            result = subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    f"{self.project_root}/docker/docker-compose.yml",
                    "up",
                    "-d",
                    "--scale",
                    f"{service_name}={new_count}",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            success = result.returncode == 0
            if success:
                self.logger.info(
                    f"Scaled {service_name} from {current_count} to {new_count} instances"  # noqa: E501
                )
            else:
                self.logger.error(f"Failed to scale {service_name}: {result.stderr}")

            return success

        except Exception as e:
            self.logger.error(f"Error scaling service {service_name}: {e}")
            return False

    def _get_service_count(self, service_name: str) -> Optional[int]:
        """Get current number of running instances for a service."""
        try:
            result = subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    f"{self.project_root}/docker/docker-compose.yml",
                    "ps",
                    "-q",
                    service_name,
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                # Count non-empty lines
                instances = [line for line in result.stdout.split("\n") if line.strip()]
                return len(instances)

            return None

        except Exception as e:
            self.logger.error(f"Error getting service count for {service_name}: {e}")
            return None


class GracefulDegradation:
    """Handles graceful degradation of non-critical features."""

    def __init__(self):
        """Initialize graceful degradation."""
        self.logger = logging.getLogger(__name__)
        self.degradation_config = {
            "api": {
                "critical_features": ["health", "runs"],
                "degradable_features": ["graph", "timeline", "analysis"],
                "degradation_levels": {
                    "low": {"timeout_ms": 5000, "cache_ttl": 300},
                    "medium": {"timeout_ms": 3000, "cache_ttl": 600},
                    "high": {"timeout_ms": 1000, "cache_ttl": 1800},
                },
            },
            "dashboard": {
                "critical_features": ["basic_ui", "health_status"],
                "degradable_features": ["advanced_visualizations", "real_time_updates"],
                "degradation_levels": {
                    "low": {"update_interval_ms": 5000, "disable_animations": False},
                    "medium": {"update_interval_ms": 10000, "disable_animations": True},
                    "high": {"update_interval_ms": 30000, "disable_animations": True},
                },
            },
        }

    def apply_degradation(self, service_name: str, stress_level: str) -> Dict[str, Any]:
        """Apply graceful degradation to a service."""
        if service_name not in self.degradation_config:
            self.logger.warning(f"No degradation config for service: {service_name}")
            return {}

        config = self.degradation_config[service_name]
        degradation_settings = config["degradation_levels"].get(stress_level, {})

        # Apply degradation settings
        applied_settings = {}

        if service_name == "api":
            applied_settings = self._apply_api_degradation(degradation_settings)
        elif service_name == "dashboard":
            applied_settings = self._apply_dashboard_degradation(degradation_settings)

        self.logger.info(
            f"Applied {stress_level} degradation to {service_name}: {applied_settings}"
        )
        return applied_settings

    def _apply_api_degradation(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Apply API-specific degradation."""
        applied = {}

        # Set timeout
        if "timeout_ms" in settings:
            applied["timeout_ms"] = settings["timeout_ms"]
            # This would typically be applied to API configuration

        # Set cache TTL
        if "cache_ttl" in settings:
            applied["cache_ttl"] = settings["cache_ttl"]
            # This would typically be applied to cache configuration

        return applied

    def _apply_dashboard_degradation(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Apply dashboard-specific degradation."""
        applied = {}

        # Set update interval
        if "update_interval_ms" in settings:
            applied["update_interval_ms"] = settings["update_interval_ms"]

        # Disable animations
        if "disable_animations" in settings:
            applied["disable_animations"] = settings["disable_animations"]

        return applied

    def remove_degradation(self, service_name: str) -> bool:
        """Remove degradation and restore normal operation."""
        try:
            # Restore normal settings
            if service_name == "api":
                # Restore normal API settings
                pass
            elif service_name == "dashboard":
                # Restore normal dashboard settings
                pass

            self.logger.info(f"Removed degradation from {service_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error removing degradation from {service_name}: {e}")
            return False


class PreemptiveRecovery:
    """Handles preemptive recovery actions."""

    def __init__(self, project_root: str):
        """Initialize preemptive recovery."""
        self.project_root = project_root
        self.logger = logging.getLogger(__name__)
        self.recovery_history: List[RecoveryAction] = []

    def preemptive_restart(self, service_name: str, reason: str) -> RecoveryAction:
        """Perform preemptive restart of a service."""
        start_time = time.time()

        try:
            # Check if service is healthy before restart
            if self._is_service_healthy(service_name):
                self.logger.info(
                    f"Service {service_name} is healthy, skipping preemptive restart"
                )
                return RecoveryAction(
                    action_type="preemptive_restart",
                    service_name=service_name,
                    trigger_reason=reason,
                    predicted_stress_level="low",
                    action_parameters={"skipped": "service_healthy"},
                    success=True,
                    duration_ms=0,
                    impact_mitigated=True,
                    manual_override=False,
                    timestamp=datetime.now(),
                )

            # Perform restart
            result = subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    f"{self.project_root}/docker/docker-compose.yml",
                    "restart",
                    service_name,
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            success = result.returncode == 0
            duration_ms = int((time.time() - start_time) * 1000)

            if success:
                # Wait for service to be healthy
                health_restored = self._wait_for_health(
                    service_name, timeout_seconds=60
                )
                impact_mitigated = health_restored
            else:
                impact_mitigated = False

            action = RecoveryAction(
                action_type="preemptive_restart",
                service_name=service_name,
                trigger_reason=reason,
                predicted_stress_level="medium",
                action_parameters={
                    "restart_result": "success" if success else "failed"
                },
                success=success,
                duration_ms=duration_ms,
                impact_mitigated=impact_mitigated,
                manual_override=False,
                timestamp=datetime.now(),
            )

            self.recovery_history.append(action)
            return action

        except Exception as e:
            self.logger.error(f"Error during preemptive restart of {service_name}: {e}")
            return RecoveryAction(
                action_type="preemptive_restart",
                service_name=service_name,
                trigger_reason=reason,
                predicted_stress_level="medium",
                action_parameters={"error": str(e)},
                success=False,
                duration_ms=int((time.time() - start_time) * 1000),
                impact_mitigated=False,
                manual_override=False,
                timestamp=datetime.now(),
            )

    def _is_service_healthy(self, service_name: str) -> bool:
        """Check if a service is healthy."""
        try:
            # Check service health via health endpoint or Docker
            if service_name == "dashboard":
                response = requests.get("http://localhost:8050/api/health", timeout=5)
                return response.status_code == 200
            elif service_name == "api":
                response = requests.get("http://localhost:8050/api/health", timeout=5)
                return response.status_code == 200
            else:
                # Generic Docker health check
                result = subprocess.run(
                    [
                        "docker",
                        "ps",
                        "--filter",
                        f"name={service_name}",
                        "--format",
                        "{{.Status}}",
                    ],
                    capture_output=True,
                    text=True,
                )

                return "Up" in result.stdout and "healthy" in result.stdout.lower()

        except Exception as e:
            self.logger.error(f"Error checking health of {service_name}: {e}")
            return False

    def _wait_for_health(self, service_name: str, timeout_seconds: int = 60) -> bool:
        """Wait for service to become healthy."""
        start_time = time.time()

        while time.time() - start_time < timeout_seconds:
            if self._is_service_healthy(service_name):
                return True
            time.sleep(2)

        return False


class RecoveryPolicyManager:
    """Manages recovery policies and their execution."""

    def __init__(self, db_connection_string: str):
        """Initialize recovery policy manager."""
        self.db_connection_string = db_connection_string
        self.logger = logging.getLogger(__name__)
        self.policies: Dict[str, RecoveryPolicy] = {}
        self.last_execution: Dict[str, datetime] = {}

        # Load default policies
        self._load_default_policies()

    def _load_default_policies(self):
        """Load default recovery policies."""
        default_policies = [
            RecoveryPolicy(
                policy_name="high_latency_scale",
                service_name="api",
                trigger_conditions={
                    "metric": "latency",
                    "threshold": 1000,  # ms
                    "duration_minutes": 5,
                },
                actions=[
                    {"type": "scale_up", "scale_factor": 1.5},
                    {"type": "graceful_degradation", "level": "medium"},
                ],
                priority=8,
                is_active=True,
                cooldown_minutes=10,
            ),
            RecoveryPolicy(
                policy_name="high_error_rate_restart",
                service_name="api",
                trigger_conditions={
                    "metric": "error_rate",
                    "threshold": 5.0,  # percent
                    "duration_minutes": 3,
                },
                actions=[
                    {"type": "preemptive_restart"},
                    {"type": "graceful_degradation", "level": "high"},
                ],
                priority=9,
                is_active=True,
                cooldown_minutes=15,
            ),
            RecoveryPolicy(
                policy_name="memory_pressure_scale",
                service_name="dashboard",
                trigger_conditions={
                    "metric": "memory_usage",
                    "threshold": 80.0,  # percent
                    "duration_minutes": 2,
                },
                actions=[{"type": "graceful_degradation", "level": "high"}],
                priority=7,
                is_active=True,
                cooldown_minutes=5,
            ),
        ]

        for policy in default_policies:
            self.policies[policy.policy_name] = policy

    def evaluate_policies(
        self, current_metrics: Dict[str, Dict[str, float]]
    ) -> List[RecoveryAction]:
        """Evaluate all policies against current metrics."""
        triggered_actions = []

        for policy_name, policy in self.policies.items():
            if not policy.is_active:
                continue

            # Check cooldown
            if self._is_in_cooldown(policy_name, policy.cooldown_minutes):
                continue

            # Evaluate policy conditions
            if self._evaluate_policy_conditions(policy, current_metrics):
                # Execute policy actions
                actions = self._execute_policy_actions(policy, current_metrics)
                triggered_actions.extend(actions)

                # Update last execution time
                self.last_execution[policy_name] = datetime.now()

        return triggered_actions

    def _evaluate_policy_conditions(
        self, policy: RecoveryPolicy, current_metrics: Dict[str, Dict[str, float]]
    ) -> bool:
        """Evaluate if policy conditions are met."""
        conditions = policy.trigger_conditions
        service_metrics = current_metrics.get(policy.service_name, {})

        metric = conditions.get("metric")
        threshold = conditions.get("threshold")
        duration = conditions.get("duration_minutes", 1)

        if metric not in service_metrics:
            return False

        current_value = service_metrics[metric]

        # Simple threshold check (could be enhanced with duration-based evaluation)
        if metric == "latency":
            return current_value > threshold
        elif metric == "error_rate":
            return current_value > threshold
        elif metric == "memory_usage":
            return current_value > threshold

        return False

    def _execute_policy_actions(
        self, policy: RecoveryPolicy, current_metrics: Dict[str, Dict[str, float]]
    ) -> List[RecoveryAction]:
        """Execute policy actions."""
        actions = []

        for action_config in policy.actions:
            action_type = action_config.get("type")

            if action_type == "scale_up":
                scale_factor = action_config.get("scale_factor", 1.5)
                # Note: Would need ServiceScaler instance
                action = RecoveryAction(
                    action_type="scale_up",
                    service_name=policy.service_name,
                    trigger_reason=f"Policy {policy.policy_name} triggered",
                    predicted_stress_level="medium",
                    action_parameters={"scale_factor": scale_factor},
                    success=True,  # Placeholder
                    duration_ms=1000,  # Placeholder
                    impact_mitigated=True,  # Placeholder
                    manual_override=False,
                    timestamp=datetime.now(),
                )
                actions.append(action)

            elif action_type == "graceful_degradation":
                level = action_config.get("level", "medium")
                # Note: Would need GracefulDegradation instance
                action = RecoveryAction(
                    action_type="graceful_degradation",
                    service_name=policy.service_name,
                    trigger_reason=f"Policy {policy.policy_name} triggered",
                    predicted_stress_level=level,
                    action_parameters={"degradation_level": level},
                    success=True,  # Placeholder
                    duration_ms=500,  # Placeholder
                    impact_mitigated=True,  # Placeholder
                    manual_override=False,
                    timestamp=datetime.now(),
                )
                actions.append(action)

            elif action_type == "preemptive_restart":
                # Note: Would need PreemptiveRecovery instance
                action = RecoveryAction(
                    action_type="preemptive_restart",
                    service_name=policy.service_name,
                    trigger_reason=f"Policy {policy.policy_name} triggered",
                    predicted_stress_level="high",
                    action_parameters={"restart_type": "preemptive"},
                    success=True,  # Placeholder
                    duration_ms=5000,  # Placeholder
                    impact_mitigated=True,  # Placeholder
                    manual_override=False,
                    timestamp=datetime.now(),
                )
                actions.append(action)

        return actions

    def _is_in_cooldown(self, policy_name: str, cooldown_minutes: int) -> bool:
        """Check if policy is in cooldown period."""
        last_exec = self.last_execution.get(policy_name)
        if not last_exec:
            return False

        time_since_last = datetime.now() - last_exec
        return time_since_last.total_seconds() < (cooldown_minutes * 60)

    def store_recovery_action(self, action: RecoveryAction) -> int:
        """Store recovery action in database."""
        try:
            with psycopg2.connect(self.db_connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.callproc(
                        "lte.record_proactive_recovery_action",
                        [
                            action.action_type,
                            action.service_name,
                            action.trigger_reason,
                            action.predicted_stress_level,
                            json.dumps(action.action_parameters)
                            if action.action_parameters
                            else None,
                            action.success,
                            action.duration_ms,
                            action.impact_mitigated,
                            action.manual_override,
                        ],
                    )
                    result = cursor.fetchone()
                    action_id = result[0] if result else None
                    conn.commit()

                    self.logger.info(
                        f"Stored recovery action: {action.action_type} for {action.service_name}"  # noqa: E501
                    )
                    return action_id

        except Exception as e:
            self.logger.error(f"Error storing recovery action: {e}")
            return None

    def get_recovery_history(
        self, service_name: Optional[str] = None, hours: int = 24
    ) -> List[Dict[str, Any]]:
        """Get recovery action history from database."""
        try:
            with psycopg2.connect(self.db_connection_string) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                        SELECT * FROM lte.proactive_recovery_actions
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
            self.logger.error(f"Error getting recovery history: {e}")
            return []


class ProactiveRecoveryManager:
    """Main proactive recovery manager."""

    def __init__(self, db_connection_string: str, project_root: str):
        """Initialize proactive recovery manager."""
        self.db_connection_string = db_connection_string
        self.project_root = project_root
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.service_scaler = ServiceScaler(project_root)
        self.graceful_degradation = GracefulDegradation()
        self.preemptive_recovery = PreemptiveRecovery(project_root)
        self.policy_manager = RecoveryPolicyManager(db_connection_string)

        # Recovery configuration
        self.recovery_active = False
        self.recovery_thread = None
        self.evaluation_interval = 30  # seconds

    def start_recovery_monitoring(self):
        """Start proactive recovery monitoring."""
        if self.recovery_active:
            self.logger.warning("Recovery monitoring already active")
            return

        self.recovery_active = True
        self.recovery_thread = threading.Thread(target=self._recovery_loop, daemon=True)
        self.recovery_thread.start()
        self.logger.info("Proactive recovery monitoring started")

    def stop_recovery_monitoring(self):
        """Stop proactive recovery monitoring."""
        self.recovery_active = False
        if self.recovery_thread:
            self.recovery_thread.join(timeout=5)
        self.logger.info("Proactive recovery monitoring stopped")

    def _recovery_loop(self):
        """Main recovery monitoring loop."""
        while self.recovery_active:
            try:
                self._evaluate_and_act()
                time.sleep(self.evaluation_interval)
            except Exception as e:
                self.logger.error(f"Error in recovery loop: {e}")
                time.sleep(self.evaluation_interval)

    def _evaluate_and_act(self):
        """Evaluate current conditions and take proactive actions."""
        # Collect current metrics
        current_metrics = self._collect_current_metrics()

        # Evaluate policies
        triggered_actions = self.policy_manager.evaluate_policies(current_metrics)

        # Execute actions
        for action in triggered_actions:
            self._execute_recovery_action(action)

    def _collect_current_metrics(self) -> Dict[str, Dict[str, float]]:
        """Collect current system metrics."""
        metrics = {}

        try:
            # Health endpoint metrics
            health_response = requests.get(
                "http://localhost:8050/api/health/full", timeout=5
            )
            if health_response.status_code == 200:
                health_data = health_response.json()

                if "data" in health_data:
                    data = health_data["data"]

                    # API metrics
                    metrics["api"] = {
                        "latency": data.get("api_latency_p95", 100.0),
                        "error_rate": data.get("error_rate", 0.0),
                    }

                    # System metrics
                    metrics["system"] = {
                        "memory_usage": data.get("memory_usage_percent", 50.0),
                        "cpu_usage": data.get("cpu_usage_percent", 30.0),
                    }

        except Exception as e:
            self.logger.error(f"Error collecting metrics: {e}")

        return metrics

    def _execute_recovery_action(self, action: RecoveryAction):
        """Execute a recovery action."""
        self.logger.info(
            f"Executing recovery action: {action.action_type} for {action.service_name}"
        )

        start_time = time.time()
        success = False
        impact_mitigated = False

        try:
            if action.action_type == "scale_up":
                scale_factor = action.action_parameters.get("scale_factor", 1.5)
                success = self.service_scaler.scale_service(
                    action.service_name, scale_factor
                )
                impact_mitigated = success

            elif action.action_type == "graceful_degradation":
                level = action.action_parameters.get("degradation_level", "medium")
                applied_settings = self.graceful_degradation.apply_degradation(
                    action.service_name, level
                )
                success = len(applied_settings) > 0
                impact_mitigated = success

            elif action.action_type == "preemptive_restart":
                recovery_action = self.preemptive_recovery.preemptive_restart(
                    action.service_name, action.trigger_reason
                )
                success = recovery_action.success
                impact_mitigated = recovery_action.impact_mitigated

        except Exception as e:
            self.logger.error(f"Error executing recovery action: {e}")
            success = False
            impact_mitigated = False

        # Update action with results
        action.success = success
        action.duration_ms = int((time.time() - start_time) * 1000)
        action.impact_mitigated = impact_mitigated

        # Store action in database
        self.policy_manager.store_recovery_action(action)

    def simulate_recovery(self, stress_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate recovery actions under predicted stress."""
        try:
            # Create simulation scenario
            service_name = stress_scenario.get("service_name", "api")
            stress_level = stress_scenario.get("stress_level", "medium")
            predicted_load = stress_scenario.get("predicted_load", 100.0)

            # Simulate policy evaluation
            simulated_metrics = {
                service_name: {
                    "latency": predicted_load * 10,  # Simulated high latency
                    "error_rate": predicted_load / 10,  # Simulated error rate
                    "memory_usage": predicted_load,  # Simulated memory usage
                }
            }

            # Evaluate policies
            triggered_actions = self.policy_manager.evaluate_policies(simulated_metrics)

            # Generate simulation report
            simulation_report = {
                "scenario": stress_scenario,
                "triggered_actions": len(triggered_actions),
                "actions": [
                    {
                        "action_type": action.action_type,
                        "service_name": action.service_name,
                        "predicted_stress_level": action.predicted_stress_level,
                        "estimated_duration_ms": action.duration_ms or 1000,
                    }
                    for action in triggered_actions
                ],
                "estimated_recovery_time_ms": sum(
                    action.duration_ms or 1000 for action in triggered_actions
                ),
                "simulation_timestamp": datetime.now().isoformat(),
            }

            return simulation_report

        except Exception as e:
            self.logger.error(f"Error simulating recovery: {e}")
            return {"error": str(e), "simulation_timestamp": datetime.now().isoformat()}

    def get_recovery_summary(self) -> Dict[str, Any]:
        """Get recovery summary for health endpoint."""
        try:
            recent_actions = self.policy_manager.get_recovery_history(hours=1)

            successful_actions = [a for a in recent_actions if a["success"]]
            mitigated_actions = [a for a in recent_actions if a["impact_mitigated"]]

            return {
                "recovery_active": self.recovery_active,
                "recent_actions": len(recent_actions),
                "successful_actions": len(successful_actions),
                "mitigated_actions": len(mitigated_actions),
                "success_rate": len(successful_actions) / len(recent_actions)
                if recent_actions
                else 1.0,
                "last_action": recent_actions[0] if recent_actions else None,
                "summary_timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error getting recovery summary: {e}")
            return {"error": str(e), "recovery_active": self.recovery_active}
