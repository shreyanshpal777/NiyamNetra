import type { Inspection } from "../../types/inspection";

interface InspectionMetaProps {
  inspection: Inspection;
}

export function InspectionMeta({ inspection }: InspectionMetaProps) {
  return (
    <dl className="grid gap-4 rounded-3xl bg-lavender p-5 sm:grid-cols-3">
      <div>
        <dt className="text-xs uppercase tracking-[0.14em] text-muted">Inspection</dt>
        <dd className="mt-2 font-semibold text-ink">{inspection.id}</dd>
      </div>
      <div>
        <dt className="text-xs uppercase tracking-[0.14em] text-muted">Category</dt>
        <dd className="mt-2 font-semibold text-ink">{inspection.category}</dd>
      </div>
      <div>
        <dt className="text-xs uppercase tracking-[0.14em] text-muted">Date</dt>
        <dd className="mt-2 font-semibold text-ink">{inspection.date}</dd>
      </div>
    </dl>
  );
}
