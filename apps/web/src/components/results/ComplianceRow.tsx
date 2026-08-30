import { AlertTriangle, CheckCircle2, ExternalLink, XCircle } from "lucide-react";
import type { RuleResult } from "../../types/inspection";
import { Button } from "../ui/button";
import { StatusBadge } from "../inspection/StatusBadge";

interface ComplianceRowProps {
  rule: RuleResult;
  onEvidence: (rule: RuleResult) => void;
}

export function ComplianceRow({ rule, onEvidence }: ComplianceRowProps) {
  const Icon =
    rule.status === "PASS" ? CheckCircle2 : rule.status === "FAIL" ? XCircle : AlertTriangle;

  return (
    <li className="grid gap-4 rounded-3xl bg-canvas p-5 sm:grid-cols-[auto_1fr_auto] sm:items-center">
      <Icon
        className={
          rule.status === "PASS"
            ? "size-6 text-pass"
            : rule.status === "FAIL"
              ? "size-6 text-fail"
              : "size-6 text-review"
        }
      />
      <div>
        <div className="flex flex-wrap items-center gap-3">
          <h3 className="text-lg font-semibold text-ink">{rule.ruleName}</h3>
          <StatusBadge status={rule.status} />
        </div>
        <p className="mt-2 text-sm leading-6 text-muted">{rule.explanation}</p>
      </div>
      <Button onClick={() => onEvidence(rule)} size="sm" type="button" variant="secondary">
        Evidence
        <ExternalLink className="size-3.5" />
      </Button>
    </li>
  );
}
