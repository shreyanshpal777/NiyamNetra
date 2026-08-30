const points = [24, 36, 30, 52, 48, 66, 61, 78, 72, 88];

export function ActivitySection() {
  const polyline = points.map((point, index) => `${index * 11},${100 - point}`).join(" ");

  return (
    <section className="rounded-[2rem] bg-white p-6 sm:p-8">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-muted">
            Inspection activity
          </p>
          <h2 className="mt-3 text-3xl font-semibold text-ink">A calm view of label throughput.</h2>
        </div>
        <p className="max-w-sm text-sm leading-6 text-muted">
          Recent captures, review rates and completed reports stay visible without turning the product into an admin dashboard.
        </p>
      </div>
      <div className="mt-10 overflow-hidden rounded-3xl bg-canvas p-5">
        <svg aria-label="Inspection activity trend" className="h-44 w-full" role="img" viewBox="0 0 100 100" preserveAspectRatio="none">
          <defs>
            <linearGradient id="activityFill" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="#bdb8da" stopOpacity="0.55" />
              <stop offset="100%" stopColor="#bdb8da" stopOpacity="0" />
            </linearGradient>
          </defs>
          <path d={`M0 100 L ${polyline} L 99 100 Z`} fill="url(#activityFill)" />
          <polyline fill="none" points={polyline} stroke="#403454" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" vectorEffect="non-scaling-stroke" />
          {points.map((point, index) => (
            <circle cx={index * 11} cy={100 - point} fill="#f9f8f5" key={index} r="1.8" stroke="#403454" strokeWidth="1.5" vectorEffect="non-scaling-stroke" />
          ))}
        </svg>
      </div>
    </section>
  );
}
