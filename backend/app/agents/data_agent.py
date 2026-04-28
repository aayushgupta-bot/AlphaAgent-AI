import logging
import re
import pandas as pd
from app.services.data_service import DataService
from app.core.exceptions import DataError

logger = logging.getLogger(__name__)

# Supports: AAPL, RELIANCE.NS, TCS.NS, BTC-USD, 005930.KS, etc.
TICKER_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9.\-]{0,14}$")

# Minimum rows needed for the feature engineering layer (MA50 window)
MIN_ROWS_REQUIRED = 60


class DataAgent:
    def __init__(self):
        self.data_service = DataService()

    async def fetch(self, ticker: str) -> pd.DataFrame:
        """
        Validates the ticker, fetches OHLCV data, and returns a clean DataFrame.

        Raises:
            DataError: On invalid ticker, empty dataset, or insufficient rows.
        """
        # ── Input validation ───────────────────────────────────────────────────
        if not ticker or not isinstance(ticker, str):
            raise DataError("Invalid ticker: must be a non-empty string.")

        ticker = ticker.strip().upper()
        if not TICKER_PATTERN.match(ticker):
            raise DataError(f"Invalid ticker format: '{ticker}'. Examples: AAPL, TSLA, RELIANCE.NS, BTC-USD")

        logger.info(f"DataAgent: Fetching data for {ticker}")

        # ── Fetch ──────────────────────────────────────────────────────────────
        try:
            df = await self.data_service.get_ohlcv(ticker, interval="1d", period="1y")
        except Exception as e:
            raise DataError(f"DataService failed for '{ticker}': {e}") from e

        # ── Output validation ──────────────────────────────────────────────────
        if df is None or df.empty:
            raise DataError(f"No market data found for ticker '{ticker}'. It may be invalid or delisted.")

        if len(df) < MIN_ROWS_REQUIRED:
            raise DataError(
                f"Insufficient data for '{ticker}': {len(df)} rows returned, "
                f"minimum required is {MIN_ROWS_REQUIRED}."
            )

        required_cols = {"open", "high", "low", "close", "volume"}
        missing = required_cols - set(df.columns)
        if missing:
            raise DataError(f"Raw data is missing required OHLCV columns: {missing}")

        logger.info(f"DataAgent: Successfully fetched {len(df)} rows for {ticker}.")
        return df
