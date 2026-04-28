"use client";

export default function Hero() {
  return (
    <section className="relative pt-8 pb-10 text-center hero-gradient overflow-hidden">

      {/* Logo */}
      <div className="animate-fade-up flex items-center justify-center gap-3 mb-6">
        <div className="relative">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-[var(--color-accent)] to-purple-500 flex items-center justify-center text-white text-xl font-bold shadow-lg shadow-[var(--color-accent-glow)]">
            α
          </div>
          {/* Pulse ring */}
          <div className="absolute inset-0 rounded-2xl border border-[var(--color-accent)] animate-[pulse-ring_2s_ease-out_infinite] opacity-40" />
        </div>
        <h1 className="text-2xl font-bold tracking-tight">
          AlphaAgent <span className="text-[var(--color-accent)]">AI</span>
        </h1>
      </div>

      {/* Tagline */}
      <h2 className="animate-fade-up stagger-1 text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight leading-tight max-w-2xl mx-auto mb-4 px-4">
        AI-powered stock intelligence.{" "}
        <span className="bg-gradient-to-r from-[var(--color-accent)] to-purple-400 bg-clip-text text-transparent">
          Not predictions—decisions.
        </span>
      </h2>

      {/* Subtext */}
      <p className="animate-fade-up stagger-2 text-base text-[var(--color-text-muted)] max-w-xl mx-auto px-4">
        Analyze stocks using multi-agent AI with real-time signals and explanations.
      </p>
    </section>
  );
}
