import type { Inspection } from "../../types/inspection";
import { InspectionCard } from "../inspection/InspectionCard";

interface RecentInspectionListProps {
  inspections: Inspection[];
}

export function RecentInspectionList({ inspections }: RecentInspectionListProps) {
  return (
    <section>
      <div className="mb-6 flex items-end justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-muted">
            Recent inspections
          </p>
          <h2 className="mt-3 text-3xl font-semibold text-ink">Evidence, ready to revisit.</h2>
        </div>
      </div>
      <div className="grid gap-3">
        {inspections.map((inspection) => (
          <InspectionCard inspection={inspection} key={inspection.id} />
        ))}
      </div>
    </section>
  );
}
