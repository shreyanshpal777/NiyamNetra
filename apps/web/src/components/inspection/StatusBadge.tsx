import { cn } from "../../lib/utils";
import type { InspectionStatus, RuleStatus } from "../../types/inspection";

type Status = InspectionStatus | RuleStatus;

const statusStyles: Record<Status, string> = {
  PASS: "bg-emerald-50 text-pass ring-emerald-100",
  REVIEW: "bg-amber-50 text-review ring-amber-100",
  WARNING: "bg-amber-50 text-review ring-amber-100",
  FAIL: "bg-rose-50 text-fail ring-rose-100",
  NOT_VERIFIABLE: "bg-stone-100 text-muted ring-stone-200",
};

interface StatusBadgeProps {
  status: Status;
  className?: string;
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const label = status === "WARNING" ? "REVIEW" : status.replace("_", " ");
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] ring-1",
        statusStyles[status],
        className,
      )}
    >
      {label}
    </span>
  );
}
