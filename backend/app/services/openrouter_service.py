"""
OpenRouter LLM Service
Handles all communication with the OpenRouter chat completions API.
"""

import os
import logging
import time
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# LLM safety controls
DEFAULT_MODEL = "openai/gpt-oss-20b:free"
MAX_TOKENS = 350          # Keep responses concise
TEMPERATURE = 0.3         # Low temperature → factual, deterministic output
REQUEST_TIMEOUT_S = 30    # Thinking model may take longer; still fails fast

FALLBACK_EXPLANATION = (
    "Explanation unavailable: the LLM service did not respond in time. "
    "Please rely on the prediction and signal fields for actionable information."
)


class OpenRouterService:
    def __init__(self):
        if not OPENROUTER_API_KEY:
            logger.warning("OpenRouterService: OPENROUTER_API_KEY is not set. LLM calls will fail gracefully.")

    async def generate_explanation(self, prompt: str) -> str:
        """
        Sends a structured prompt to OpenRouter and returns the generated text.

        Args:
            prompt: The fully-constructed analyst prompt string.

        Returns:
            LLM response text, or FALLBACK_EXPLANATION on any failure.
        """
        if not OPENROUTER_API_KEY:
            logger.error("OpenRouterService: No API key configured — returning fallback.")
            return FALLBACK_EXPLANATION

        prompt_tokens_approx = len(prompt.split())
        logger.info(
            f"OpenRouterService: Sending prompt (~{prompt_tokens_approx} words) "
            f"to model '{DEFAULT_MODEL}'"
        )

        payload = {
            "model": DEFAULT_MODEL,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional financial analyst. "
                        "Your role is to explain stock analysis results clearly and factually. "
                        "You must ONLY reference the data provided in the prompt. "
                        "Never guarantee outcomes. Never invent external information."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://alpha-agent-ai.dev",
            "X-Title": "AlphaAgent AI",
        }

        t0 = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_S) as client:
                response = await client.post(
                    OPENROUTER_API_URL,
                    json=payload,
                    headers=headers,
                )

            elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

            if response.status_code != 200:
                logger.error(
                    f"OpenRouterService: API returned HTTP {response.status_code}. "
                    f"Body: {response.text[:300]}"
                )
                return FALLBACK_EXPLANATION

            data = response.json()
            explanation = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
                .strip()
            )

            if not explanation:
                logger.warning("OpenRouterService: Empty content in API response.")
                return FALLBACK_EXPLANATION

            logger.info(f"OpenRouterService: Response received in {elapsed_ms}ms ({len(explanation)} chars)")
            return explanation

        except httpx.TimeoutException:
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
            logger.error(f"OpenRouterService: Request timed out after {elapsed_ms}ms.")
            return FALLBACK_EXPLANATION

        except httpx.RequestError as e:
            logger.error(f"OpenRouterService: Network error — {e}")
            return FALLBACK_EXPLANATION

        except Exception as e:
            logger.error(f"OpenRouterService: Unexpected error — {e}")
            return FALLBACK_EXPLANATION
