import type { RuleResult } from "../../types/inspection";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "../ui/sheet";
import { StatusBadge } from "../inspection/StatusBadge";

interface EvidenceDrawerProps {
  open: boolean;
  rule?: RuleResult;
  onOpenChange: (open: boolean) => void;
}

export function EvidenceDrawer({ open, rule, onOpenChange }: EvidenceDrawerProps) {
  return (
    <Sheet onOpenChange={onOpenChange} open={open}>
      <SheetContent className="max-w-md">
        <SheetHeader>
          <SheetTitle>{rule?.ruleName ?? "Evidence"}</SheetTitle>
          <SheetDescription>Detected source evidence used by the compliance engine.</SheetDescription>
        </SheetHeader>
        {rule && (
          <div className="grid gap-5">
            <StatusBadge status={rule.status} />
            <div className="rounded-3xl bg-lavender p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.14em] text-muted">Detected text</p>
              <p className="mt-3 text-2xl font-semibold text-ink">"{rule.detectedText}"</p>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-3xl bg-white p-5 ring-1 ring-line">
                <p className="text-xs font-semibold uppercase tracking-[0.14em] text-muted">OCR confidence</p>
                <p className="mt-3 text-2xl font-semibold text-ink">{rule.confidence}%</p>
              </div>
              <div className="rounded-3xl bg-white p-5 ring-1 ring-line">
                <p className="text-xs font-semibold uppercase tracking-[0.14em] text-muted">Measured height</p>
                <p className="mt-3 text-2xl font-semibold text-ink">{rule.measuredHeight ?? "—"}</p>
              </div>
            </div>
            <div className="relative aspect-[4/3] overflow-hidden rounded-3xl bg-[#d8d4ec]">
              <div className="absolute inset-8 rounded-2xl bg-white/75 shadow-xl" />
              <div
                className="absolute rounded-lg border-2 border-plum bg-plum/10"
                style={{
                  left: `${Math.max(rule.evidenceRegion.x - 4, 6)}%`,
                  top: `${Math.max(rule.evidenceRegion.y - 4, 8)}%`,
                  width: `${rule.evidenceRegion.width + 8}%`,
                  height: `${rule.evidenceRegion.height + 8}%`,
                }}
              />
            </div>
          </div>
        )}
      </SheetContent>
    </Sheet>
  );
}
