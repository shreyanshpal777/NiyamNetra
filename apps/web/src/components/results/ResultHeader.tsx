import type { Inspection } from "../../types/inspection";
import { Button } from "../ui/button";
import { ScoreDisplay } from "./ScoreDisplay";

interface ResultHeaderProps {
  inspection: Inspection;
}

export function ResultHeader({ inspection }: ResultHeaderProps) {
  return (
    <section className="grid gap-6 py-10 lg:grid-cols-[1fr_320px] lg:items-end">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">
          Inspection result
        </p>
        <h1 className="display-heading mt-5 max-w-3xl text-5xl font-semibold text-ink sm:text-7xl">
          {inspection.productName}
        </h1>
        <p className="mt-6 max-w-xl text-base leading-7 text-muted">
          Evidence-backed compliance result generated from OCR, measurement, semantic extraction and deterministic rule checks.
        </p>
        <div className="mt-7 flex flex-wrap gap-3">
          <Button>Download PDF</Button>
          <Button variant="secondary">Share evidence</Button>
        </div>
      </div>
      <ScoreDisplay score={inspection.score} status={inspection.status} />
    </section>
  );
}
