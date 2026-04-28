"""
Custom structured exception system for AlphaAgent AI pipeline.
All exceptions carry a type + message that map cleanly to API error responses.
"""


class AlphaAgentError(Exception):
    """Base exception for all AlphaAgent pipeline errors."""
    error_type: str = "AgentError"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def to_dict(self) -> dict:
        return {"type": self.error_type, "message": self.message}

    def __repr__(self) -> str:
        return f"{self.error_type}: {self.message}"


# ── Specific error classes ────────────────────────────────────────────────────

class DataError(AlphaAgentError):
    """Raised when data fetching or validation fails in DataAgent / DataService."""
    error_type = "DataError"


class FeatureError(AlphaAgentError):
    """Raised when feature engineering fails or required columns are missing."""
    error_type = "FeatureError"


class PredictionError(AlphaAgentError):
    """Raised when ML inference fails or returns an invalid prediction."""
    error_type = "PredictionError"


class SignalError(AlphaAgentError):
    """Raised when the SignalAgent receives invalid prediction input."""
    error_type = "SignalError"
