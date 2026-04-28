"use client";

const FEATURES = [
  {
    icon: "📊",
    title: "Real-time Analysis",
    description: "Live OHLCV data with RSI, MACD, Bollinger Bands, and 50+ day moving averages.",
  },
  {
    icon: "🤖",
    title: "AI Signal Engine",
    description: "XGBoost ML model generates BUY, SELL, or HOLD signals with confidence scores.",
  },
  {
    icon: "🧠",
    title: "Smart Explanation",
    description: "LLM-powered analysis explains every signal using only computed data. No hallucinations.",
  },
];

export default function FeatureHighlights() {
  return (
    <div className="animate-fade-up stagger-4 grid grid-cols-1 sm:grid-cols-3 gap-4 mb-12">
      {FEATURES.map((f, i) => (
        <div
          key={i}
          className="glass-card p-6 text-center group"
        >
          <div className="text-3xl mb-3 group-hover:animate-float">{f.icon}</div>
          <h3 className="text-sm font-semibold text-[var(--color-text-primary)] mb-1.5">
            {f.title}
          </h3>
          <p className="text-xs leading-relaxed text-[var(--color-text-muted)]">
            {f.description}
          </p>
        </div>
      ))}
    </div>
  );
}
