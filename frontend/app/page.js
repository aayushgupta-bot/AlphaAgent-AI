"use client";

// Import React hooks for state management and performance optimization
import { useState, useCallback, useRef } from "react";

// Import UI components used in dashboard
import Hero from "@/components/Hero";
import TickerInput from "@/components/TickerInput";
import SuggestedStocks from "@/components/SuggestedStocks";
import FeatureHighlights from "@/components/FeatureHighlights";
import StockChart from "@/components/StockChart";
import PredictionCard from "@/components/PredictionCard";
import SignalCard from "@/components/SignalCard";
import ExplanationPanel from "@/components/ExplanationPanel";
import MetadataBar from "@/components/MetadataBar";
import LoadingSkeleton from "@/components/LoadingSkeleton";

// Import API service functions for fetching prediction and feature data
import { getPrediction, getFeatures } from "@/services/api";

// Main dashboard component handling UI and business logic
export default function Dashboard() {

  // State variables to manage API data, loading state, errors, and selected ticker
  const [data, setData] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTicker, setActiveTicker] = useState("");

  // Ref used for scrolling to results section after analysis
  const resultsRef = useRef(null);

  const handleAnalyze = useCallback(async (ticker) => {
    setIsLoading(true);
    setError(null);
    setData(null);
    setChartData([]);
    setActiveTicker(ticker);

    // Smooth scroll to results area
    setTimeout(() => {
      resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);

    try {
      const [predictionRes, featuresRes] = await Promise.all([
        getPrediction(ticker),
        getFeatures(ticker).catch(() => null),
      ]);

      setData(predictionRes);

      if (featuresRes?.sample_rows) {
        const rows = featuresRes.sample_rows.map((row) => ({
          date: row.Date?.split(" ")[0] || "",
          close: row.close,
        }));
        setChartData(rows);
      }
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  return (
    <div className="min-h-screen">
      {/* ── Hero ──────────────────────────────────────────────────────── */}
      <Hero />

      {/* ── Main content ──────────────────────────────────────────────── */}
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 -mt-2 pb-20">
        {/* Ticker Input */}
        <section className="mb-6">
          <TickerInput onSubmit={handleAnalyze} isLoading={isLoading} />
        </section>

        {/* Suggested Stocks */}
        <SuggestedStocks onSelect={handleAnalyze} isLoading={isLoading} />

        {/* Feature Highlights — only show when no results */}
        {!data && !isLoading && !error && <FeatureHighlights />}

        {/* ── Results zone ────────────────────────────────────────────── */}
        <div ref={resultsRef}>
          {/* Error */}
          {error && (
            <div className="animate-fade-up mb-6 glass-card border-[var(--color-sell)]/20 px-5 py-4 flex items-start gap-3">
              <span className="text-lg mt-0.5">⚠️</span>
              <div>
                <p className="text-sm font-semibold text-[var(--color-sell)] mb-0.5">Analysis Failed</p>
                <p className="text-xs text-[var(--color-text-muted)]">{error}</p>
              </div>
            </div>
          )}

          {/* Loading */}
          {isLoading && <LoadingSkeleton />}

          {/* Results */}
          {data && !isLoading && (
            <>
              <MetadataBar metadata={data.metadata} ticker={data.ticker} />

              {/* Chart — full width */}
              {chartData.length > 0 && (
                <div className="mb-5">
                  <StockChart
                    data={chartData}
                    predictedPrice={data.prediction?.predicted_price}
                  />
                </div>
              )}

              {/* Prediction + Signal — side by side */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
                <PredictionCard prediction={data.prediction} />
                <SignalCard signal={data.signal} />
              </div>

              {/* Explanation — full width */}
              <ExplanationPanel explanation={data.explanation} />
            </>
          )}

          {/* Empty state */}
          {!data && !isLoading && !error && (
            <div className="text-center py-16">
              <div className="text-4xl mb-4 animate-float">📈</div>
              <p className="text-sm text-[var(--color-text-muted)]">
                Start by analyzing a stock above
              </p>
            </div>
          )}
        </div>
      </main>

      {/* ── Footer ────────────────────────────────────────────────────── */}
      <footer className="text-center py-6 border-t border-[var(--color-border)]">
        <p className="text-[10px] uppercase tracking-[0.25em] text-[var(--color-text-muted)]">
          AlphaAgent AI · Multi-Agent Intelligence · Not Financial Advice
        </p>
      </footer>
    </div>
  );
}
