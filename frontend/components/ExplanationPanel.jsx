"use client";

export default function ExplanationPanel({ explanation }) {
  if (!explanation) return null;

  const paragraphs = explanation.split(/\n\n+/).filter(Boolean);

  return (
    <div className="animate-fade-up stagger-5 glass-card p-6 sm:p-8">
      <div className="flex items-center gap-2 mb-6">
        <span className="text-lg">🧠</span>
        <h2 className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--color-text-muted)]">
          AI Analysis
        </h2>
      </div>

      <div className="space-y-5">
        {paragraphs.map((p, i) => {
          const headerMatch = p.match(/^\*\*(.+?)\*\*\s*\n?([\s\S]*)/);

          if (headerMatch) {
            return (
              <div key={i} className="group">
                <h3 className="text-sm font-semibold mb-1.5 flex items-center gap-2">
                  <span className="w-1 h-4 rounded-full bg-gradient-to-b from-[var(--color-accent)] to-purple-500 inline-block" />
                  <span className="bg-gradient-to-r from-[var(--color-accent)] to-purple-400 bg-clip-text text-transparent">
                    {headerMatch[1]}
                  </span>
                </h3>
                <p className="text-sm leading-[1.8] text-[var(--color-text-secondary)] pl-3 border-l border-[var(--color-border)]">
                  {headerMatch[2].trim()}
                </p>
              </div>
            );
          }

          return (
            <p key={i} className="text-sm leading-[1.8] text-[var(--color-text-secondary)]">
              {p.trim()}
            </p>
          );
        })}
      </div>
    </div>
  );
}
