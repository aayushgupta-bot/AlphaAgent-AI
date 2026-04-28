import logging
import pandas as pd
from app.services.indicator_service import IndicatorService
from app.core.exceptions import FeatureError

logger = logging.getLogger(__name__)

REQUIRED_FEATURE_COLS = [
    "close", "ma10", "ma20", "ma50",
    "rsi", "macd", "macd_signal",
    "bb_upper", "bb_lower",
    "returns", "volatility",
]


class FeatureAgent:
    def __init__(self):
        self.indicator_service = IndicatorService()

    async def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies technical indicators to raw OHLCV data.
        Drops NaN rows, then validates that all required features are present.

        Args:
            df: Clean OHLCV DataFrame from DataAgent.

        Returns:
            Feature-enriched DataFrame ready for ML inference.

        Raises:
            FeatureError: If input is invalid or required features are missing post-calculation.
        """
        # ── Input validation ───────────────────────────────────────────────────
        if df is None or not isinstance(df, pd.DataFrame) or df.empty:
            raise FeatureError("FeatureAgent received an empty or invalid DataFrame.")

        logger.info(f"FeatureAgent: Calculating indicators on {len(df)} rows.")

        # ── Calculate indicators ───────────────────────────────────────────────
        try:
            features_df = await self.indicator_service.calculate_indicators(df)
        except Exception as e:
            raise FeatureError(f"Indicator calculation failed: {e}") from e

        # Drop NaN rows from rolling windows (MA50, RSI, etc.)
        pre_drop = len(features_df)
        features_df = features_df.dropna()
        post_drop = len(features_df)
        logger.info(f"FeatureAgent: Dropped {pre_drop - post_drop} NaN rows. Remaining: {post_drop}")

        # ── Output validation ──────────────────────────────────────────────────
        if features_df.empty:
            raise FeatureError(
                "All rows were NaN after indicator calculation. "
                "The dataset likely has insufficient history."
            )

        missing_cols = [c for c in REQUIRED_FEATURE_COLS if c not in features_df.columns]
        if missing_cols:
            raise FeatureError(f"Required feature columns are missing: {missing_cols}")

        logger.info(f"FeatureAgent: Feature engineering complete. Shape: {features_df.shape}")
        return features_df
