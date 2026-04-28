"use client";

export default function MetadataBar({ metadata, ticker }) {
  if (!metadata) return null;

  const steps = metadata.step_timings_ms
    ? Object.entries(metadata.step_timings_ms)
    : [];

  return (
    <div className="animate-fade-up flex flex-wrap items-center gap-x-1.5 gap-y-1.5 mb-6">
      {ticker && (
        <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest bg-[var(--color-accent-glow)] text-[var(--color-accent-hover)]">
          {ticker}
        </span>
      )}
      {metadata.total_pipeline_ms && (
        <span className="inline-flex items-center px-2.5 py-1 rounded-full text-[10px] tracking-wide bg-[var(--color-surface-glass)] text-[var(--color-text-muted)] border border-[var(--color-border)]">
          Pipeline {metadata.total_pipeline_ms.toFixed(0)}ms
        </span>
      )}
      {steps.map(([step, ms]) => (
        <span
          key={step}
          className="inline-flex items-center px-2.5 py-1 rounded-full text-[10px] tracking-wide bg-[var(--color-surface-glass)] text-[var(--color-text-muted)] border border-[var(--color-border)]"
        >
          {step.replace("_agent", "")} {ms < 1 ? "<1" : ms.toFixed(0)}ms
        </span>
      ))}
    </div>
  );
}
