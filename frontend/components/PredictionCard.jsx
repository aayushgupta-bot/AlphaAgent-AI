"use client";

export default function PredictionCard({ prediction }) {
  if (!prediction) return null;

  const dir = prediction.direction;
  const isUp = dir === "UP";
  const isNeutral = dir === "NEUTRAL";
  const arrow = isNeutral ? "→" : isUp ? "↑" : "↓";
  const dirColor = isNeutral ? "var(--color-hold)" : isUp ? "var(--color-buy)" : "var(--color-sell)";
  const dirBg = isNeutral ? "var(--color-hold-bg)" : isUp ? "var(--color-buy-bg)" : "var(--color-sell-bg)";
  const dirGlow = isNeutral ? "transparent" : isUp ? "var(--color-buy-glow)" : "var(--color-sell-glow)";

  return (
    <div className="animate-fade-up stagger-2 glass-card p-6">
      <h2 className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--color-text-muted)] mb-5">
        Prediction
      </h2>

      {/* Price */}
      <div className="text-4xl font-bold tracking-tighter mb-1">
        ${prediction.predicted_price?.toFixed(2)}
      </div>
      <div className="text-xs text-[var(--color-text-muted)] mb-4">predicted next close</div>

      {/* Direction badge */}
      <div className="flex items-center gap-3 mb-5">
        <span
          className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-bold tracking-wide"
          style={{
            color: dirColor,
            backgroundColor: dirBg,
            boxShadow: `0 0 12px ${dirGlow}`,
          }}
        >
          <span className="text-sm">{arrow}</span>
          {prediction.direction}
        </span>
        <span className="text-sm text-[var(--color-text-secondary)]">
          <span className="text-[var(--color-text-muted)]">Confidence</span>{" "}
          <strong className="text-[var(--color-text-primary)]">{(prediction.confidence * 100).toFixed(0)}%</strong>
        </span>
      </div>

      {/* Range bar */}
      <div className="bg-[var(--color-surface)] rounded-xl p-3">
        <div className="flex justify-between text-[10px] uppercase tracking-widest text-[var(--color-text-muted)] mb-1">
          <span>Low</span>
          <span>High</span>
        </div>
        <div className="flex justify-between text-sm font-semibold">
          <span>${prediction.range?.[0]?.toFixed(2)}</span>
          <span>${prediction.range?.[1]?.toFixed(2)}</span>
        </div>
        <div className="mt-2 h-1 rounded-full bg-[var(--color-border)] overflow-hidden">
          <div
            className="h-full rounded-full"
            style={{
              width: "100%",
              background: `linear-gradient(90deg, ${isUp ? "var(--color-buy)" : "var(--color-sell)"} 0%, var(--color-accent) 100%)`,
              opacity: 0.6,
            }}
          />
        </div>
      </div>
    </div>
  );
}
