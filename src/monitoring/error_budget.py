#!/usr/bin/env python3
"""
Error Budget Monitoring Module
==============================

This module provides error budget tracking, SLO/SLI monitoring, and recovery
action management for the Living Truth Engine.

Features:
- Error budget calculation and tracking
- SLO/SLI monitoring
- Recovery action logging
- Chaos test result tracking
- Health endpoint integration
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


@dataclass
class ErrorBudgetMetric:
    """Error budget metric data structure."""

    service_name: str
    metric_type: str
    metric_value: float
    slo_target: float
    error_budget_consumed: float
    error_budget_remaining: float
    timestamp: datetime


@dataclass
class RecoveryAction:
    """Recovery action data structure."""

    action_type: str
    service_name: str
    trigger_reason: str
    success: bool
    duration_ms: Optional[int]
    error_message: Optional[str]
    manual_override: bool
    timestamp: datetime


@dataclass
class ChaosTestResult:
    """Chaos test result data structure."""

    test_type: str
    test_duration_ms: int
    recovery_time_ms: Optional[int]
    recovery_success: bool
    slo_violation: bool
    details: Optional[Dict[str, Any]]
    timestamp: datetime


class ErrorBudgetMonitor:
    """Error budget monitoring and management."""

    def __init__(self, db_connection_string: str):
        """Initialize the error budget monitor."""
        self.db_connection_string = db_connection_string
        self.logger = logging.getLogger(__name__)

    def get_db_connection(self):
        """Get database connection."""
        return psycopg2.connect(self.db_connection_string)

    def record_metric(
        self, service_name: str, metric_type: str, metric_value: float
    ) -> int:
        """
        Record an error budget metric.

        Args:
            service_name: Name of the service
            metric_type: Type of metric (availability, latency_p95, error_rate)
            metric_value: Current metric value

        Returns:
            ID of the recorded metric
        """
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.callproc(
                        "lte.record_error_budget_metric",
                        [service_name, metric_type, metric_value],
                    )
                    result = cursor.fetchone()
                    metric_id = result[0] if result else None

                    self.logger.info(
                        f"Recorded metric: {service_name}/{metric_type}={metric_value}"
                    )
                    return metric_id

        except Exception as e:
            self.logger.error(f"Error recording metric: {e}")
            raise

    def get_error_budget_status(
        self, service_name: str, metric_type: str, window_days: int = 30
    ) -> Dict[str, Any]:
        """
        Get current error budget status for a service and metric.

        Args:
            service_name: Name of the service
            metric_type: Type of metric
            window_days: Rolling window in days

        Returns:
            Error budget status dictionary
        """
        try:
            with self.get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.callproc(
                        "lte.calculate_error_budget_consumption",
                        [service_name, metric_type, window_days],
                    )
                    result = cursor.fetchone()

                    if result:
                        return {
                            "service_name": service_name,
                            "metric_type": metric_type,
                            "error_budget_consumed": float(
                                result["error_budget_consumed"]
                            ),
                            "error_budget_remaining": float(
                                result["error_budget_remaining"]
                            ),
                            "current_value": float(result["current_value"]),
                            "slo_target": float(result["slo_target"]),
                            "window_days": window_days,
                            "timestamp": datetime.now().isoformat(),
                        }
                    else:
                        return {
                            "service_name": service_name,
                            "metric_type": metric_type,
                            "error_budget_consumed": 0.0,
                            "error_budget_remaining": 0.0,
                            "current_value": 0.0,
                            "slo_target": 0.0,
                            "window_days": window_days,
                            "timestamp": datetime.now().isoformat(),
                            "error": "No SLO definition found",
                        }

        except Exception as e:
            self.logger.error(f"Error getting error budget status: {e}")
            return {
                "service_name": service_name,
                "metric_type": metric_type,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def get_all_error_budgets(self) -> Dict[str, Any]:
        """
        Get error budget status for all services and metrics.

        Returns:
            Dictionary with error budget status for all services
        """
        try:
            with self.get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Get all SLO definitions
                    cursor.execute("""
                        SELECT service_name, metric_type, slo_target, error_budget_percentage
                        FROM lte.slo_definitions
                        WHERE is_active = TRUE
                        ORDER BY service_name, metric_type
                    """)  # noqa: E501
                    slo_definitions = cursor.fetchall()

                    budgets = {}
                    for slo in slo_definitions:
                        service_name = slo["service_name"]
                        metric_type = slo["metric_type"]

                        if service_name not in budgets:
                            budgets[service_name] = {}

                        budget_status = self.get_error_budget_status(
                            service_name, metric_type
                        )
                        budgets[service_name][metric_type] = budget_status

                    return {
                        "error_budgets": budgets,
                        "total_services": len(budgets),
                        "timestamp": datetime.now().isoformat(),
                    }

        except Exception as e:
            self.logger.error(f"Error getting all error budgets: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def record_recovery_action(
        self,
        action_type: str,
        service_name: str,
        trigger_reason: str,
        success: bool,
        duration_ms: Optional[int] = None,
        error_message: Optional[str] = None,
        manual_override: bool = False,
    ) -> int:
        """
        Record a recovery action.

        Args:
            action_type: Type of recovery action
            service_name: Name of the service
            trigger_reason: Reason for the recovery action
            success: Whether the recovery was successful
            duration_ms: Duration of the recovery action
            error_message: Error message if recovery failed
            manual_override: Whether this was a manual override

        Returns:
            ID of the recorded recovery action
        """
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.callproc(
                        "lte.record_recovery_action",
                        [
                            action_type,
                            service_name,
                            trigger_reason,
                            success,
                            duration_ms,
                            error_message,
                            manual_override,
                        ],
                    )
                    result = cursor.fetchone()
                    action_id = result[0] if result else None

                    self.logger.info(
                        f"Recorded recovery action: {action_type} for {service_name}"
                    )
                    return action_id

        except Exception as e:
            self.logger.error(f"Error recording recovery action: {e}")
            raise

    def get_recent_recovery_actions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent recovery actions.

        Args:
            limit: Maximum number of actions to return

        Returns:
            List of recent recovery actions
        """
        try:
            with self.get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM lte.recovery_actions
                        ORDER BY timestamp DESC
                        LIMIT %s
                    """,
                        (limit,),
                    )

                    actions = []
                    for row in cursor.fetchall():
                        actions.append(
                            {
                                "id": row["id"],
                                "action_type": row["action_type"],
                                "service_name": row["service_name"],
                                "trigger_reason": row["trigger_reason"],
                                "success": row["success"],
                                "duration_ms": row["duration_ms"],
                                "error_message": row["error_message"],
                                "manual_override": row["manual_override"],
                                "timestamp": row["timestamp"].isoformat(),
                            }
                        )

                    return actions

        except Exception as e:
            self.logger.error(f"Error getting recent recovery actions: {e}")
            return []

    def record_chaos_test_result(
        self,
        test_type: str,
        test_duration_ms: int,
        recovery_time_ms: Optional[int] = None,
        recovery_success: bool = False,
        slo_violation: bool = False,
        details: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Record a chaos test result.

        Args:
            test_type: Type of chaos test
            test_duration_ms: Duration of the test
            recovery_time_ms: Time taken to recover
            recovery_success: Whether recovery was successful
            slo_violation: Whether SLO was violated
            details: Additional test details

        Returns:
            ID of the recorded chaos test result
        """
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    details_json = json.dumps(details) if details else None
                    cursor.callproc(
                        "lte.record_chaos_test_result",
                        [
                            test_type,
                            test_duration_ms,
                            recovery_time_ms,
                            recovery_success,
                            slo_violation,
                            details_json,
                        ],
                    )
                    result = cursor.fetchone()
                    test_id = result[0] if result else None

                    self.logger.info(f"Recorded chaos test result: {test_type}")
                    return test_id

        except Exception as e:
            self.logger.error(f"Error recording chaos test result: {e}")
            raise

    def get_chaos_test_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get chaos test history.

        Args:
            limit: Maximum number of tests to return

        Returns:
            List of chaos test results
        """
        try:
            with self.get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM lte.chaos_test_results
                        ORDER BY timestamp DESC
                        LIMIT %s
                    """,
                        (limit,),
                    )

                    tests = []
                    for row in cursor.fetchall():
                        tests.append(
                            {
                                "id": row["id"],
                                "test_type": row["test_type"],
                                "test_duration_ms": row["test_duration_ms"],
                                "recovery_time_ms": row["recovery_time_ms"],
                                "recovery_success": row["recovery_success"],
                                "slo_violation": row["slo_violation"],
                                "details": row["details"],
                                "timestamp": row["timestamp"].isoformat(),
                            }
                        )

                    return tests

        except Exception as e:
            self.logger.error(f"Error getting chaos test history: {e}")
            return []

    def check_error_budget_threshold(
        self, service_name: str, metric_type: str, threshold_percentage: float = 80.0
    ) -> bool:
        """
        Check if error budget consumption exceeds threshold.

        Args:
            service_name: Name of the service
            metric_type: Type of metric
            threshold_percentage: Threshold percentage (default 80%)

        Returns:
            True if threshold exceeded, False otherwise
        """
        try:
            budget_status = self.get_error_budget_status(service_name, metric_type)

            if "error" in budget_status:
                self.logger.warning(
                    f"Error getting budget status: {budget_status['error']}"
                )
                return False

            consumed_percentage = budget_status["error_budget_consumed"]
            return consumed_percentage >= threshold_percentage

        except Exception as e:
            self.logger.error(f"Error checking error budget threshold: {e}")
            return False

    def get_health_summary(self) -> Dict[str, Any]:
        """
        Get error budget health summary for health endpoint.

        Returns:
            Health summary dictionary
        """
        try:
            all_budgets = self.get_all_error_budgets()
            recent_actions = self.get_recent_recovery_actions(5)
            recent_tests = self.get_chaos_test_history(5)

            # Calculate overall health
            total_services = all_budgets.get("total_services", 0)
            critical_services = 0

            for service_name, metrics in all_budgets.get("error_budgets", {}).items():
                for metric_type, budget in metrics.items():
                    if "error_budget_consumed" in budget:
                        if budget["error_budget_consumed"] >= 80.0:  # 80% threshold
                            critical_services += 1

            return {
                "error_budget_remaining": all_budgets,
                "last_recovery_action": recent_actions[0] if recent_actions else None,
                "recent_recovery_actions": recent_actions,
                "recent_chaos_tests": recent_tests,
                "total_services": total_services,
                "critical_services": critical_services,
                "health_status": "critical" if critical_services > 0 else "healthy",
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error getting health summary: {e}")
            return {
                "error": str(e),
                "health_status": "unknown",
                "timestamp": datetime.now().isoformat(),
            }
