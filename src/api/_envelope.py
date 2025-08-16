"""
API Response Envelope Helpers

Standardizes all API responses to use the envelope format:
{status: "ok"|"error", data?: any, error?: {code: string, message: string}}
"""

from typing import Any, Dict, Optional, Union


def ok(data: Any) -> Dict[str, Any]:
    """Return successful response with data."""
    return {"status": "ok", "data": data}


def err(code: str, message: str) -> Dict[str, Any]:
    """Return error response with code and message."""
    return {"status": "error", "error": {"code": code, "message": message}}


def validate_envelope(response: Dict[str, Any]) -> bool:
    """Validate that a response follows the envelope format."""
    if not isinstance(response, dict):
        return False

    if "status" not in response:
        return False

    if response["status"] == "ok":
        return "data" in response
    elif response["status"] == "error":
        return "error" in response and isinstance(response["error"], dict)
    else:
        return False
