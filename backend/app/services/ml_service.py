import os
import logging
import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/xgb.pkl")
FEATURE_COLS_PATH = os.path.join(os.path.dirname(__file__), "../models/feature_cols.pkl")

# Direction thresholds (in predicted return magnitude)
RETURN_THRESHOLD = 0.002  # 0.2% — below this is NEUTRAL


class MLService:
    def __init__(self):
        self.model = None
        self.feature_cols = None
        self._load_model()

    def _load_model(self):
        """Lazily loads the XGBoost model and feature column list from disk."""
        try:
            self.model = joblib.load(MODEL_PATH)
            self.feature_cols = joblib.load(FEATURE_COLS_PATH)
            logger.info("MLService: Model and feature columns loaded successfully.")
        except FileNotFoundError:
            logger.warning(
                "MLService: Model file not found. "
                "Run `python -m app.models.train_model` to train and save the model."
            )
        except Exception as e:
            logger.error(f"MLService: Failed to load model: {e}")

    def run_inference(self, df: pd.DataFrame) -> dict:
        """
        Runs XGBoost regression inference on the latest feature row.
        The model predicts next-day percentage return, not absolute price.

        Returns:
            dict with predicted_price, predicted_return, direction, confidence, and range.
        """
        if self.model is None:
            raise ValueError("Model is not loaded. Train and save the model first.")

        if df is None or df.empty:
            raise ValueError("Empty features DataFrame passed to MLService.")

        # Align columns to match training features
        missing_cols = [c for c in self.feature_cols if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Features DataFrame is missing columns: {missing_cols}")

        # Use only the latest row for prediction
        latest_row = df[self.feature_cols].iloc[[-1]]
        current_close = float(df["close"].iloc[-1])
        current_volatility = float(df["volatility"].iloc[-1])

        # ── Prediction (returns-based) ────────────────────────────────────
        predicted_return = float(self.model.predict(latest_row)[0])

        # Convert return → predicted price
        predicted_price = current_close * (1 + predicted_return)

        # ── Direction ─────────────────────────────────────────────────────
        if predicted_return > RETURN_THRESHOLD:
            direction = "UP"
        elif predicted_return < -RETURN_THRESHOLD:
            direction = "DOWN"
        else:
            direction = "NEUTRAL"

        # ── Confidence ────────────────────────────────────────────────────
        # Normalize |predicted_return| against recent volatility.
        # A return that matches 1x daily vol = moderate confidence.
        if current_volatility > 0:
            raw_confidence = abs(predicted_return) / current_volatility
        else:
            raw_confidence = 0.5

        confidence = round(float(np.clip(raw_confidence, 0.05, 0.99)), 4)

        # ── Price range ───────────────────────────────────────────────────
        volatility_band = current_close * current_volatility
        price_range = [
            round(predicted_price - volatility_band, 2),
            round(predicted_price + volatility_band, 2),
        ]

        logger.info(
            f"MLService: predicted_return={predicted_return:.6f}, "
            f"volatility={current_volatility:.6f}, "
            f"confidence={confidence:.4f}, direction={direction}"
        )

        return {
            "predicted_price": round(predicted_price, 2),
            "predicted_return": round(predicted_return, 6),
            "direction": direction,
            "confidence": confidence,
            "range": price_range,
        }
