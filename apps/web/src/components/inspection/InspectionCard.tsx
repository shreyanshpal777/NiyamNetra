import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";
import type { Inspection } from "../../types/inspection";
import { StatusBadge } from "./StatusBadge";

interface InspectionCardProps {
  inspection: Inspection;
}

export function InspectionCard({ inspection }: InspectionCardProps) {
  return (
    <Link
      className="group grid gap-4 rounded-3xl border border-line bg-white px-5 py-5 transition hover:-translate-y-0.5 hover:shadow-lg sm:grid-cols-[1fr_auto] sm:items-center"
      to={`/inspection/${inspection.id}`}
    >
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-muted">
          {inspection.id}
        </p>
        <h3 className="mt-2 text-xl font-semibold text-ink">{inspection.productName}</h3>
        <p className="mt-1 text-sm text-muted">{inspection.date}</p>
      </div>
      <div className="flex items-center justify-between gap-5 sm:justify-end">
        <div className="text-right">
          <p className="text-2xl font-semibold text-ink">{inspection.score || "—"}</p>
          <StatusBadge status={inspection.status} />
        </div>
        <span className="flex size-9 items-center justify-center rounded-full bg-lavender text-plum transition group-hover:bg-plum group-hover:text-white">
          <ArrowUpRight className="size-4" />
        </span>
      </div>
    </Link>
  );
}
