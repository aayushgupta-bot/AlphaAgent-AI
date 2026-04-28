"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] backdrop-blur-lg px-4 py-2.5 text-xs shadow-2xl">
      <div className="text-[var(--color-text-muted)] mb-0.5">{d.date}</div>
      <div className="font-bold text-base text-[var(--color-text-primary)]">
        ${d.close?.toFixed(2)}
      </div>
    </div>
  );
}

export default function StockChart({ data, predictedPrice }) {
  if (!data || data.length === 0) return null;

  const minPrice = Math.min(...data.map((d) => d.close)) * 0.995;
  const maxPrice = Math.max(...data.map((d) => d.close)) * 1.005;

  return (
    <div className="animate-fade-up stagger-1 glass-card p-6">
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--color-text-muted)]">
          Price History
        </h2>
        <span className="text-[10px] tracking-widest text-[var(--color-text-muted)] uppercase">
          {data.length} days
        </span>
      </div>

      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={data} margin={{ top: 4, right: 8, bottom: 0, left: 0 }}>
          <defs>
            <linearGradient id="priceGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="var(--color-accent)" stopOpacity={0.3} />
              <stop offset="60%" stopColor="var(--color-accent)" stopOpacity={0.05} />
              <stop offset="100%" stopColor="var(--color-accent)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis
            dataKey="date"
            tick={{ fill: "var(--color-text-muted)", fontSize: 10 }}
            axisLine={false}
            tickLine={false}
            interval="preserveStartEnd"
            minTickGap={60}
          />
          <YAxis
            domain={[minPrice, maxPrice]}
            tick={{ fill: "var(--color-text-muted)", fontSize: 10 }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(v) => `$${v.toFixed(0)}`}
            width={48}
          />
          <Tooltip content={<CustomTooltip />} />
          {predictedPrice && (
            <ReferenceLine
              y={predictedPrice}
              stroke="var(--color-accent)"
              strokeDasharray="8 6"
              strokeWidth={1}
              strokeOpacity={0.6}
              label={{
                value: `Predicted $${predictedPrice.toFixed(2)}`,
                fill: "var(--color-accent)",
                fontSize: 10,
                fontWeight: 600,
                position: "right",
              }}
            />
          )}
          <Area
            type="monotone"
            dataKey="close"
            stroke="var(--color-accent)"
            strokeWidth={2}
            fill="url(#priceGrad)"
            dot={false}
            animationDuration={1000}
            animationEasing="ease-out"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
