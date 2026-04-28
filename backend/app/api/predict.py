from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.agents.orchestrator import OrchestratorAgent

router = APIRouter()
orchestrator = OrchestratorAgent()


# ── Response schemas ───────────────────────────────────────────────────────────

class PredictionSchema(BaseModel):
    predicted_price: float
    predicted_return: Optional[float] = None
    direction: str        # "UP" | "DOWN" | "NEUTRAL"
    confidence: float
    range: List[float]    # [low, high]


class SignalSchema(BaseModel):
    action: str           # "BUY" | "SELL" | "HOLD"
    strength: str         # "WEAK" | "MODERATE" | "STRONG"
    confidence: float
    reason: str


class MetadataSchema(BaseModel):
    timestamp: str
    total_pipeline_ms: float
    step_timings_ms: dict


class PredictResponse(BaseModel):
    ticker: str
    status: str
    prediction: PredictionSchema
    signal: SignalSchema
    explanation: Optional[str] = None
    metadata: MetadataSchema


class ErrorResponse(BaseModel):
    ticker: str
    status: str
    error: dict
    metadata: dict


# ── Route ──────────────────────────────────────────────────────────────────────

@router.get("/", response_model=PredictResponse)
async def get_prediction(ticker: str):
    """
    Triggers the full multi-agent pipeline for a given stock ticker.
    Returns a structured prediction, actionable signal, and execution metadata.
    """
    result = await orchestrator.run_analysis(ticker)

    if result.get("status") != "success":
        error_info = result.get("error", {})
        raise HTTPException(
            status_code=400,
            detail={
                "ticker": result["ticker"],
                "error": error_info,
                "metadata": result.get("metadata", {}),
            },
        )

    return PredictResponse(
        ticker=result["ticker"],
        status=result["status"],
        prediction=PredictionSchema(**result["prediction"]),
        signal=SignalSchema(**result["signal"]),
        explanation=result.get("explanation"),
        metadata=MetadataSchema(**result["metadata"]),
    )
