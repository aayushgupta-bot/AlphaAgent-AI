import logging
import time
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Any, Optional

import pandas as pd

from app.agents.data_agent import DataAgent
from app.agents.feature_agent import FeatureAgent
from app.agents.ml_agent import MLAgent
from app.agents.signal_agent import SignalAgent
from app.agents.rag_agent import RAGAgent
from app.agents.explanation_agent import ExplanationAgent
from app.core.exceptions import AlphaAgentError, DataError, FeatureError, PredictionError, SignalError

logger = logging.getLogger(__name__)


@dataclass
class PipelineState:
    """Tracks all intermediate outputs and metadata as the pipeline executes."""
    ticker: str
    status: str = "running"           # running | success | failure
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    data: Optional[pd.DataFrame] = None
    features: Optional[pd.DataFrame] = None
    prediction: Optional[dict] = None
    signal: Optional[dict] = None
    error: Optional[dict] = None
    step_timings_ms: dict = field(default_factory=dict)


class OrchestratorAgent:
    def __init__(self):
        self.data_agent = DataAgent()
        self.feature_agent = FeatureAgent()
        self.ml_agent = MLAgent()
        self.signal_agent = SignalAgent()
        self.rag_agent = RAGAgent()
        self.explanation_agent = ExplanationAgent()

    async def run_analysis(self, ticker: str) -> dict:
        """
        Executes the full multi-agent analysis pipeline for a given ticker.

        Pipeline:
            1. DataAgent → 2. FeatureAgent → 3. MLAgent → 4. SignalAgent → 5. ExplanationAgent

        Returns:
            Structured dict with prediction, signal, and metadata.
        """
        state = PipelineState(ticker=ticker.upper().strip())
        pipeline_start = time.perf_counter()

        logger.info(f"Orchestrator: ── Starting pipeline for {state.ticker} ──")

        try:
            # ── Step 1: Data ───────────────────────────────────────────────────
            state.data = await self._run_step(
                state, "data_agent",
                self.data_agent.fetch(state.ticker)
            )

            # ── Step 2: Features ───────────────────────────────────────────────
            state.features = await self._run_step(
                state, "feature_agent",
                self.feature_agent.process(state.data)
            )

            # ── Step 3: ML Prediction ──────────────────────────────────────────
            state.prediction = await self._run_step(
                state, "ml_agent",
                self.ml_agent.predict(state.features)
            )

            # ── Step 4: Signal Generation ──────────────────────────────────────
            current_price = float(state.features["close"].iloc[-1])
            current_volatility = float(state.features["volatility"].iloc[-1])
            state.signal = await self._run_step(
                state, "signal_agent",
                self.signal_agent.generate(state.prediction, current_price, current_volatility)
            )

            # ── Step 5: LLM Explanation ────────────────────────────────────────
            # ExplanationAgent is non-blocking — a failure here never kills the pipeline.
            # It receives only computed data; it cannot alter prediction or signal.
            explanation = await self._run_step(
                state, "explanation_agent",
                self.explanation_agent.explain(
                    ticker=state.ticker,
                    prediction=state.prediction,
                    signal=state.signal,
                    features=state.features,
                )
            )

        except AlphaAgentError as e:
            state.status = "failure"
            state.error = e.to_dict()
            total_ms = round((time.perf_counter() - pipeline_start) * 1000, 2)
            logger.error(f"Orchestrator: Pipeline failed — {e}")
            return self._build_error_response(state, total_ms)

        state.status = "success"
        total_ms = round((time.perf_counter() - pipeline_start) * 1000, 2)
        logger.info(f"Orchestrator: ── Pipeline complete for {state.ticker} in {total_ms}ms ──")

        return {
            "ticker": state.ticker,
            "status": "success",
            "prediction": {
                "predicted_price": state.prediction["predicted_price"],
                "predicted_return": state.prediction.get("predicted_return", 0.0),
                "direction": state.prediction["direction"],
                "confidence": state.prediction["confidence"],
                "range": state.prediction["range"],
            },
            "signal": state.signal,
            "explanation": explanation,
            "metadata": {
                "timestamp": state.timestamp,
                "total_pipeline_ms": total_ms,
                "step_timings_ms": state.step_timings_ms,
            },
        }

    async def _run_step(self, state: PipelineState, step_name: str, coro) -> Any:
        """
        Runs a single awaitable step, measures its duration, and stores
        it in the pipeline state. Raises AlphaAgentError on failure.
        """
        logger.info(f"Orchestrator: → Running step [{step_name}]")
        t0 = time.perf_counter()
        try:
            result = await coro
            elapsed = round((time.perf_counter() - t0) * 1000, 2)
            state.step_timings_ms[step_name] = elapsed
            logger.info(f"Orchestrator: ✓ [{step_name}] completed in {elapsed}ms")
            return result
        except AlphaAgentError:
            elapsed = round((time.perf_counter() - t0) * 1000, 2)
            state.step_timings_ms[step_name] = elapsed
            raise  # re-raise for top-level handler
        except Exception as e:
            elapsed = round((time.perf_counter() - t0) * 1000, 2)
            state.step_timings_ms[step_name] = elapsed
            # Wrap unexpected exceptions in the base error type
            raise AlphaAgentError(f"Unexpected error in [{step_name}]: {e}") from e

    def _build_error_response(self, state: PipelineState, total_ms: float) -> dict:
        return {
            "ticker": state.ticker,
            "status": "failure",
            "error": state.error,
            "metadata": {
                "timestamp": state.timestamp,
                "total_pipeline_ms": total_ms,
                "step_timings_ms": state.step_timings_ms,
            },
        }
