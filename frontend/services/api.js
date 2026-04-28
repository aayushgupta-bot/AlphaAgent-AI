const API_BASE = process.env.NEXT_PUBLIC_API_URL 
  || "http://localhost:8000/api";

/**
 * Fetches prediction, signal, and explanation for a given ticker.
 * @param {string} ticker — Stock ticker symbol (e.g. "AAPL")
 * @returns {Promise<object>} — Structured API response
 */
export async function getPrediction(ticker) {
  const res = await fetch(`${API_BASE}/predict/?ticker=${encodeURIComponent(ticker)}`);

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    const detail = errorData?.detail;
    const msg =
      typeof detail === "object"
        ? detail?.error?.message || JSON.stringify(detail)
        : detail || `Request failed (HTTP ${res.status})`;
    throw new Error(msg);
  }

  return res.json();
}

/**
 * Fetches feature data for a given ticker.
 * @param {string} ticker
 * @returns {Promise<object>}
 */
export async function getFeatures(ticker) {
  const res = await fetch(`${API_BASE}/stock/features?ticker=${encodeURIComponent(ticker)}`);
  if (!res.ok) throw new Error(`Features request failed (HTTP ${res.status})`);
  return res.json();
}
