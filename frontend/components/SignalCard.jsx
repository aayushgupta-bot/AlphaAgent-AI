"use client";

export default function SignalCard({ signal }) {
  if (!signal) return null;

  const palette = {
    BUY:  { color: "var(--color-buy)",  bg: "var(--color-buy-bg)",  glow: "var(--color-buy-glow)",  icon: "🟢" },
    SELL: { color: "var(--color-sell)", bg: "var(--color-sell-bg)", glow: "var(--color-sell-glow)", icon: "🔴" },
    HOLD: { color: "var(--color-hold)", bg: "var(--color-hold-bg)", glow: "transparent",           icon: "⚪" },
  };
  const p = palette[signal.action] || palette.HOLD;

  return (
    <div className="animate-fade-up stagger-3 glass-card p-6">
      <h2 className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--color-text-muted)] mb-5">
        Signal
      </h2>

      {/* Action badge */}
      <div className="flex items-center gap-3 mb-5">
        <div
          className="px-5 py-2.5 rounded-xl text-2xl font-black tracking-wider"
          style={{
            color: p.color,
            backgroundColor: p.bg,
            boxShadow: `0 0 24px ${p.glow}`,
          }}
        >
          {signal.action}
        </div>
        <span className="text-lg">{p.icon}</span>
      </div>

      {/* Stats */}
      <div className="space-y-3 mb-5">
        <div className="flex items-center justify-between">
          <span className="text-xs text-[var(--color-text-muted)]">Strength</span>
          <span className="text-sm font-bold text-[var(--color-text-primary)] tracking-wide">
            {signal.strength}
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs text-[var(--color-text-muted)]">Confidence</span>
          <span className="text-sm font-bold text-[var(--color-text-primary)]">
            {(signal.confidence * 100).toFixed(0)}%
          </span>
        </div>
        {/* Confidence bar */}
        <div className="h-1.5 rounded-full bg-[var(--color-surface)] overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-700"
            style={{
              width: `${(signal.confidence * 100).toFixed(0)}%`,
              backgroundColor: p.color,
              boxShadow: `0 0 8px ${p.glow}`,
            }}
          />
        </div>
      </div>

      {/* Reason */}
      <div className="bg-[var(--color-surface)] rounded-xl p-3.5">
        <p className="text-xs leading-relaxed text-[var(--color-text-muted)]">
          {signal.reason}
        </p>
      </div>
    </div>
  );
}
