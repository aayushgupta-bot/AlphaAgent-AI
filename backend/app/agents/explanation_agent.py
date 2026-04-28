"""
Explanation Agent
Constructs a grounded analyst prompt from structured pipeline outputs
and returns a human-readable explanation from the LLM.
"""

import logging
import pandas as pd
from app.services.openrouter_service import OpenRouterService

logger = logging.getLogger(__name__)

# Hard cap on feature values included in the prompt to avoid token bloat
MAX_PROMPT_FEATURE_LINES = 8


class ExplanationAgent:
    def __init__(self):
        self.llm_service = OpenRouterService()

    async def explain(
        self,
        ticker: str,
        prediction: dict,
        signal: dict,
        features: pd.DataFrame,
    ) -> str:
        """
        Builds a structured analyst prompt and returns the LLM explanation.

        The LLM receives ONLY data computed by the ML and signal layers —
        it cannot modify, override, or second-guess those outputs.

        Args:
            ticker:     Stock ticker symbol.
            prediction: MLAgent output dict (predicted_price, direction, confidence, range).
            signal:     SignalAgent output dict (action, strength, confidence, reason).
            features:   Feature DataFrame from FeatureAgent (latest row is used).

        Returns:
            Plain-text explanation string.
        """
        try:
            prompt = self._build_prompt(ticker, prediction, signal, features)
            explanation = await self.llm_service.generate_explanation(prompt)
            return explanation
        except Exception as e:
            logger.error(f"ExplanationAgent: Failed to generate explanation — {e}")
            return "Explanation unavailable due to an internal error."

    def _build_prompt(
        self,
        ticker: str,
        prediction: dict,
        signal: dict,
        features: pd.DataFrame,
    ) -> str:
        """
        Constructs a tightly structured prompt using only factual, computed data.
        No external information is ever injected.
        """
        # ── Extract latest feature values ──────────────────────────────────────
        latest = features.iloc[-1]

        current_price = round(float(latest.get("close", 0)), 2)
        rsi           = round(float(latest.get("rsi", 0)), 2)
        ma10          = round(float(latest.get("ma10", 0)), 2)
        ma20          = round(float(latest.get("ma20", 0)), 2)
        ma50          = round(float(latest.get("ma50", 0)), 2)
        macd          = round(float(latest.get("macd", 0)), 4)
        macd_signal   = round(float(latest.get("macd_signal", 0)), 4)
        bb_upper      = round(float(latest.get("bb_upper", 0)), 2)
        bb_lower      = round(float(latest.get("bb_lower", 0)), 2)
        volatility    = round(float(latest.get("volatility", 0)), 4)
        returns       = round(float(latest.get("returns", 0)) * 100, 3)  # as %

        # ── Prediction & signal fields ─────────────────────────────────────────
        direction       = prediction.get("direction", "N/A")
        confidence      = round(float(prediction.get("confidence", 0)) * 100, 1)
        predicted_price = round(float(prediction.get("predicted_price", 0)), 2)
        price_range     = prediction.get("range", [0, 0])
        action          = signal.get("action", "N/A")
        strength        = signal.get("strength", "N/A")

        # ── Construct prompt ───────────────────────────────────────────────────
        prompt = f"""Analyze the following quantitative stock data and provide a structured explanation.

--- INPUT DATA ---
Ticker:            {ticker}
Current Price:     ${current_price}
Predicted Price:   ${predicted_price} ({direction})
Prediction Range:  ${price_range[0]} – ${price_range[1]}
Model Confidence:  {confidence}%

Signal:            {action} [{strength}]

Technical Indicators:
  RSI (14-period):   {rsi}  {"(Overbought >70)" if rsi > 70 else "(Oversold <30)" if rsi < 30 else "(Neutral)"}
  MA10:              ${ma10}
  MA20:              ${ma20}
  MA50:              ${ma50}
  MACD:              {macd}  |  Signal Line: {macd_signal}  {"(Bullish crossover)" if macd > macd_signal else "(Bearish crossover)"}
  Bollinger Upper:   ${bb_upper}
  Bollinger Lower:   ${bb_lower}
  Daily Volatility:  {volatility:.4f}  ({returns}% daily return)
--- END DATA ---

Explain the following in exactly 3 short paragraphs:
1. Current trend: Interpret RSI, moving averages, and MACD in plain English.
2. Signal justification: Why does this data support a {action} signal?
3. Short-term outlook: What should the investor watch for next? State this is not financial advice.

Rules:
- Be concise. Each paragraph: 2–3 sentences maximum.
- Only reference the data provided above.
- Do NOT invent earnings, news, or external events.
- Do NOT guarantee any price outcome.
"""
        logger.info(f"ExplanationAgent: Prompt built ({len(prompt)} chars) for {ticker}")
        return prompt
