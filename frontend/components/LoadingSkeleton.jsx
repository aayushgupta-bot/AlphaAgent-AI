"use client";

export default function LoadingSkeleton() {
  return (
    <div className="animate-fade-in space-y-5">
      {/* Loader animation */}
      <div className="flex flex-col items-center justify-center py-10 gap-4">
        <div className="relative w-12 h-12">
          <div className="absolute inset-0 rounded-full border-2 border-[var(--color-border)] border-t-[var(--color-accent)] animate-spin" />
          <div className="absolute inset-2 rounded-full border-2 border-[var(--color-border)] border-b-purple-500 animate-spin [animation-direction:reverse] [animation-duration:1.5s]" />
        </div>
        <p className="text-sm text-[var(--color-text-muted)] tracking-wide">
          Agents are analyzing the market…
        </p>
        <div className="flex gap-1 mt-1">
          {["data", "features", "ml", "signal", "explanation"].map((step, i) => (
            <span
              key={step}
              className="text-[9px] uppercase tracking-widest text-[var(--color-text-muted)] px-2 py-0.5 rounded-full border border-[var(--color-border)] animate-pulse"
              style={{ animationDelay: `${i * 200}ms` }}
            >
              {step}
            </span>
          ))}
        </div>
      </div>

      {/* Skeleton placeholders */}
      <div className="skeleton h-72 w-full" />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="skeleton h-52" />
        <div className="skeleton h-52" />
      </div>
      <div className="skeleton h-48 w-full" />
    </div>
  );
}
