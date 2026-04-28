import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class IndicatorService:
    async def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates MA10, MA20, MA50, RSI, MACD, Bollinger Bands, Returns, Volatility.
        Returns a new DataFrame with indicators appended.
        """
        if df.empty or len(df) < 50:
            logger.warning("DataFrame is empty or too small to calculate all indicators (need at least 50 periods).")
            # We still attempt to calculate what we can, but MA50 will be mostly NaN
            
        data = df.copy()
        
        try:
            # Moving Averages
            data['ma10'] = data['close'].rolling(window=10).mean()
            data['ma20'] = data['close'].rolling(window=20).mean()
            data['ma50'] = data['close'].rolling(window=50).mean()
            
            # RSI (14 periods)
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['rsi'] = 100 - (100 / (1 + rs))
            
            # MACD (12, 26, 9)
            ema12 = data['close'].ewm(span=12, adjust=False).mean()
            ema26 = data['close'].ewm(span=26, adjust=False).mean()
            data['macd'] = ema12 - ema26
            data['macd_signal'] = data['macd'].ewm(span=9, adjust=False).mean()
            
            # Bollinger Bands (20 periods)
            std20 = data['close'].rolling(window=20).std()
            data['bb_upper'] = data['ma20'] + (std20 * 2)
            data['bb_lower'] = data['ma20'] - (std20 * 2)
            
            # Returns (percentage change)
            data['returns'] = data['close'].pct_change()
            
            # Volatility (rolling std of returns, 20 periods)
            data['volatility'] = data['returns'].rolling(window=20).std()
            
            return data
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            raise
