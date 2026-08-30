import { StatusBadge } from "../inspection/StatusBadge";
import type { InspectionStatus } from "../../types/inspection";

interface ScoreDisplayProps {
  score: number;
  status: InspectionStatus;
}

export function ScoreDisplay({ score, status }: ScoreDisplayProps) {
  return (
    <div className="rounded-[2rem] bg-plum p-6 text-white sm:p-8">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-white/55">Compliance score</p>
      <div className="mt-8 flex items-end gap-2">
        <span className="text-6xl font-semibold leading-none">{score}</span>
        <span className="pb-2 text-lg text-white/55">/ 100</span>
      </div>
      <StatusBadge className="mt-5 bg-white/10 text-white ring-white/15" status={status} />
    </div>
  );
}
