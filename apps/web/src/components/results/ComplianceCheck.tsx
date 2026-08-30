import { useState } from "react";
import type { RuleResult } from "../../types/inspection";
import { ComplianceRow } from "./ComplianceRow";
import { EvidenceDrawer } from "./EvidenceDrawer";

interface ComplianceCheckProps {
  rules: RuleResult[];
}

export function ComplianceCheck({ rules }: ComplianceCheckProps) {
  const [selectedRule, setSelectedRule] = useState<RuleResult | undefined>();

  return (
    <section className="rounded-[2rem] bg-white p-6 sm:p-8">
      <h2 className="text-2xl font-semibold text-ink">Compliance check</h2>
      <ol className="mt-8 grid gap-3">
        {rules.map((rule) => (
          <ComplianceRow key={rule.id} onEvidence={setSelectedRule} rule={rule} />
        ))}
      </ol>
      <EvidenceDrawer
        onOpenChange={(open) => {
          if (!open) setSelectedRule(undefined);
        }}
        open={Boolean(selectedRule)}
        rule={selectedRule}
      />
    </section>
  );
}
