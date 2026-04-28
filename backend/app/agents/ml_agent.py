import logging
import time
import pandas as pd
from app.services.ml_service import MLService
from app.core.exceptions import PredictionError

logger = logging.getLogger(__name__)

VALID_DIRECTIONS = {"UP", "DOWN", "NEUTRAL"}


class MLAgent:
    def __init__(self):
        # Model is loaded once at startup to minimize I/O on each request
        self.ml_service = MLService()

    async def predict(self, df: pd.DataFrame) -> dict:
        """
        Runs XGBoost inference on the feature DataFrame and returns a
        validated, structured prediction dict.

        Args:
            df: Feature DataFrame from FeatureAgent.

        Returns:
            dict: {predicted_price, predicted_return, direction, confidence, range}

        Raises:
            PredictionError: On invalid input, missing model, or bad inference output.
        """
        # ── Input validation ───────────────────────────────────────────────────
        if df is None or not isinstance(df, pd.DataFrame) or df.empty:
            raise PredictionError("MLAgent received an empty or invalid features DataFrame.")

        logger.info(f"MLAgent: Running inference on {len(df)} feature rows.")
        start = time.perf_counter()

        # ── Inference ─────────────────────────────────────────────────────────
        try:
            result = self.ml_service.run_inference(df)
        except ValueError as e:
            raise PredictionError(str(e)) from e
        except Exception as e:
            raise PredictionError(f"Unexpected inference error: {e}") from e

        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        # ── Output validation ──────────────────────────────────────────────────
        if result.get("direction") not in VALID_DIRECTIONS:
            raise PredictionError(
                f"Invalid direction value: '{result.get('direction')}'. "
                f"Expected one of {VALID_DIRECTIONS}."
            )
        if not (0.0 <= result.get("confidence", -1) <= 1.0):
            raise PredictionError(
                f"Confidence value out of range: {result.get('confidence')}. Must be in [0.0, 1.0]."
            )
        if not isinstance(result.get("range"), list) or len(result["range"]) != 2:
            raise PredictionError("Prediction range must be a list of exactly two floats [low, high].")

        logger.info(
            f"MLAgent: Prediction complete in {elapsed_ms}ms — "
            f"return={result.get('predicted_return', 'N/A')}, "
            f"direction={result['direction']}, confidence={result['confidence']}"
        )
        result["inference_ms"] = elapsed_ms
        return result
