"use client";

import { useState } from "react";

export default function TickerInput({ onSubmit, isLoading }) {
  const [value, setValue] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    const ticker = value.trim().toUpperCase();
    if (!ticker || isLoading) return;
    onSubmit(ticker);
  }

  function handleChange(e) {
    setValue(e.target.value.toUpperCase().replace(/[^A-Z0-9.\-]/g, "").slice(0, 15));
  }

  return (
    <form onSubmit={handleSubmit} className="animate-fade-up stagger-2 flex gap-3 w-full max-w-lg mx-auto">
      <div className="relative flex-1">
        <svg
          className="absolute left-4 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-[var(--color-text-muted)]"
          fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          id="ticker-input"
          type="text"
          value={value}
          onChange={handleChange}
          placeholder="Search stocks (AAPL, TSLA, RELIANCE.NS)"
          maxLength={12}
          disabled={isLoading}
          className="w-full pl-11 pr-4 py-4 rounded-2xl
                     bg-[var(--color-surface-glass)] backdrop-blur-xl
                     border border-[var(--color-border)]
                     text-[var(--color-text-primary)] text-base font-medium tracking-wide
                     placeholder:text-[var(--color-text-muted)]
                     outline-none transition-all duration-300
                     focus:border-[var(--color-accent)] focus:shadow-[0_0_20px_var(--color-accent-glow)]
                     disabled:opacity-40"
        />
      </div>
      <button
        id="submit-btn"
        type="submit"
        disabled={isLoading || !value.trim()}
        className="px-8 py-4 rounded-2xl font-semibold text-sm tracking-wide
                   bg-gradient-to-r from-[var(--color-accent)] to-purple-500 text-white
                   shadow-lg shadow-[var(--color-accent-glow)]
                   hover:shadow-[0_0_30px_var(--color-accent-glow)] hover:scale-[1.02]
                   active:scale-[0.97]
                   transition-all duration-300
                   disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:scale-100
                   cursor-pointer"
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Analyzing…
          </span>
        ) : (
          "Analyze"
        )}
      </button>
    </form>
  );
}
