import { CheckCircle2, FileWarning, XCircle } from "lucide-react";

export function ComplianceOverview() {
  return (
    <div className="grid gap-3 sm:grid-cols-3">
      <div className="rounded-3xl bg-emerald-50 p-5 text-pass">
        <CheckCircle2 className="size-5" />
        <p className="mt-8 text-3xl font-semibold">12</p>
        <p className="mt-1 text-sm text-muted">Rules passing</p>
      </div>
      <div className="rounded-3xl bg-amber-50 p-5 text-review">
        <FileWarning className="size-5" />
        <p className="mt-8 text-3xl font-semibold">3</p>
        <p className="mt-1 text-sm text-muted">Need review</p>
      </div>
      <div className="rounded-3xl bg-rose-50 p-5 text-fail">
        <XCircle className="size-5" />
        <p className="mt-8 text-3xl font-semibold">1</p>
        <p className="mt-1 text-sm text-muted">Failed checks</p>
      </div>
    </div>
  );
}
