"use client";

const POPULAR_STOCKS = [
  { ticker: "AAPL",        label: "Apple" },
  { ticker: "TSLA",        label: "Tesla" },
  { ticker: "MSFT",        label: "Microsoft" },
  { ticker: "NVDA",        label: "Nvidia" },
  { ticker: "RELIANCE.NS", label: "Reliance" },
  { ticker: "TCS.NS",      label: "TCS" },
];

export default function SuggestedStocks({ onSelect, isLoading }) {
  return (
    <div className="animate-fade-up stagger-3 text-center mb-10">
      <p className="text-xs font-semibold uppercase tracking-widest text-[var(--color-text-muted)] mb-4">
        Try Popular Stocks · Global &amp; Indian
      </p>
      <div className="flex flex-wrap justify-center gap-2">
        {POPULAR_STOCKS.map((s) => (
          <button
            key={s.ticker}
            onClick={() => !isLoading && onSelect(s.ticker)}
            disabled={isLoading}
            className="stock-pill disabled:opacity-30 disabled:cursor-not-allowed"
          >
            {s.ticker}
          </button>
        ))}
      </div>
    </div>
  );
}
