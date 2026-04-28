import yfinance as yf
import pandas as pd
import logging
import asyncio

logger = logging.getLogger(__name__)

class DataService:
    async def get_ohlcv(self, ticker: str, interval: str = "1d", period: str = "1mo") -> pd.DataFrame:
        """
        Fetches OHLCV data using yfinance.
        Runs in a threadpool to avoid blocking the async event loop.
        """
        try:
            # yfinance is synchronous, so we run it in a thread
            df = await asyncio.to_thread(self._fetch_yfinance, ticker, interval, period)
            return df
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            raise

    def _fetch_yfinance(self, ticker: str, interval: str, period: str) -> pd.DataFrame:
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(period=period, interval=interval)
        
        if df.empty:
            logger.warning(f"No data returned for ticker {ticker} with period {period} and interval {interval}")
            return pd.DataFrame()
            
        # Clean column names
        df.columns = df.columns.str.lower()
        
        # Handle missing values (forward fill then backward fill)
        df.ffill(inplace=True)
        df.bfill(inplace=True)
        
        return df
