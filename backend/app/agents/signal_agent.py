import logging
from app.core.exceptions import SignalError

logger = logging.getLogger(__name__)

# ── Thresholds ─────────────────────────────────────────────────────────────────
HOLD_CONFIDENCE = 0.40       # Below this → HOLD regardless of direction
WEAK_UPPER = 0.60
MODERATE_UPPER = 0.80


class SignalAgent:
    """
    Converts a validated ML prediction into an actionable trading signal.

    Signal Logic:
        direction == NEUTRAL           → HOLD
        confidence < 0.40              → HOLD   (not enough conviction)
        direction == UP  + c >= 0.40   → BUY
        direction == DOWN + c >= 0.40  → SELL

    Strength:
        0.40 <= c < 0.60   → WEAK
        0.60 <= c < 0.80   → MODERATE
        c >= 0.80           → STRONG
    """

    async def generate(self, prediction: dict, current_price: float, volatility: float) -> dict:
        """
        Generates a structured trading signal from the ML prediction.

        Args:
            prediction: Output dict from MLAgent (direction, confidence, range, predicted_return).
            current_price: Latest close price for context.
            volatility: Latest rolling volatility value.

        Returns:
            dict: {action, strength, confidence, reason}

        Raises:
            SignalError: If prediction dict is missing required keys.
        """
        # ── Input validation ───────────────────────────────────────────────────
        required_keys = {"direction", "confidence", "predicted_price", "range"}
        missing = required_keys - set(prediction.keys())
        if missing:
            raise SignalError(f"Prediction dict is missing keys: {missing}")

        direction: str = prediction["direction"]
        confidence: float = prediction["confidence"]
        predicted_price: float = prediction["predicted_price"]
        predicted_return: float = prediction.get("predicted_return", 0.0)
        price_range: list = prediction["range"]

        if not isinstance(confidence, (int, float)) or not (0.0 <= confidence <= 1.0):
            raise SignalError(f"Invalid confidence value: {confidence}")

        logger.info(
            f"SignalAgent: direction={direction}, confidence={confidence:.4f}, "
            f"predicted_return={predicted_return:.6f}, current_price={current_price:.2f}, "
            f"volatility={volatility:.6f}"
        )

        # ── Determine strength ─────────────────────────────────────────────────
        if confidence < WEAK_UPPER:
            strength = "WEAK"
        elif confidence < MODERATE_UPPER:
            strength = "MODERATE"
        else:
            strength = "STRONG"

        # ── Signal determination ───────────────────────────────────────────────
        if direction == "NEUTRAL" or confidence < HOLD_CONFIDENCE:
            action = "HOLD"
            strength = "WEAK"
            reason = (
                f"Predicted return ({predicted_return:+.2%}) is near zero or "
                f"confidence ({confidence:.0%}) is below the {HOLD_CONFIDENCE:.0%} "
                f"threshold. No clear directional edge — holding is advised."
            )
        elif direction == "UP":
            action = "BUY"
            reason = (
                f"Model predicts an upward move to ${predicted_price:.2f} "
                f"(return: {predicted_return:+.2%}, "
                f"range: ${price_range[0]:.2f}–${price_range[1]:.2f}) "
                f"with {confidence:.0%} confidence. "
                f"Current volatility: {volatility:.4f}. Signal strength: {strength}."
            )
        else:  # direction == "DOWN"
            action = "SELL"
            reason = (
                f"Model predicts a downward move to ${predicted_price:.2f} "
                f"(return: {predicted_return:+.2%}, "
                f"range: ${price_range[0]:.2f}–${price_range[1]:.2f}) "
                f"with {confidence:.0%} confidence. "
                f"Current volatility: {volatility:.4f}. Signal strength: {strength}."
            )

        signal = {
            "action": action,
            "strength": strength,
            "confidence": round(confidence, 4),
            "reason": reason,
        }

        logger.info(f"SignalAgent: Signal generated — {action} [{strength}]")
        return signal
