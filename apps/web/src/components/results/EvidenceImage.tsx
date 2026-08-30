import { useState } from "react";
import type { Inspection } from "../../types/inspection";
import { Button } from "../ui/button";

interface EvidenceImageProps {
  inspection: Inspection;
}

export function EvidenceImage({ inspection }: EvidenceImageProps) {
  const [mode, setMode] = useState<"original" | "annotated">("annotated");

  return (
    <section className="rounded-[2rem] bg-white p-4 sm:p-5">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3 px-1">
        <h2 className="text-2xl font-semibold text-ink">Visual evidence</h2>
        <div className="rounded-full bg-canvas p-1">
          <Button
            onClick={() => setMode("original")}
            size="sm"
            type="button"
            variant={mode === "original" ? "default" : "ghost"}
          >
            Original
          </Button>
          <Button
            onClick={() => setMode("annotated")}
            size="sm"
            type="button"
            variant={mode === "annotated" ? "default" : "ghost"}
          >
            Annotated
          </Button>
        </div>
      </div>
      <div className="relative aspect-[16/10] overflow-hidden rounded-[1.5rem] bg-lavender">
        {inspection.imageUrl ? (
          <img alt="Package label evidence" className="h-full w-full object-cover" src={inspection.imageUrl} />
        ) : (
          <div className="relative h-full w-full bg-[#d9d5ee]">
            <div className="absolute left-[10%] top-[14%] h-[72%] w-[44%] rotate-[-4deg] rounded-[1.4rem] bg-[#f8f6ef] shadow-2xl">
              <div className="mx-8 mt-10 h-6 rounded-full bg-plum" />
              <div className="mx-8 mt-8 h-4 w-3/4 rounded-full bg-lavender-deep" />
              <div className="mx-8 mt-4 h-4 w-2/3 rounded-full bg-lavender-deep" />
              <div className="absolute bottom-10 left-8 right-8 h-20 rounded-2xl bg-white/70" />
            </div>
            <div className="absolute bottom-[17%] right-[18%] grid size-14 grid-cols-2 gap-1 bg-white p-1">
              <span className="bg-ink" />
              <span className="bg-ink" />
              <span className="bg-ink" />
              <span className="bg-white" />
            </div>
          </div>
        )}
        {mode === "annotated" && (
          <div className="absolute inset-0">
            {inspection.ruleResults.slice(0, 5).map((rule) => (
              <span
                className="absolute rounded-lg border-2 border-white/80 bg-white/10 shadow-[0_0_0_1px_rgba(64,52,84,0.4)]"
                key={rule.id}
                style={{
                  left: `${rule.evidenceRegion.x}%`,
                  top: `${rule.evidenceRegion.y}%`,
                  width: `${rule.evidenceRegion.width}%`,
                  height: `${rule.evidenceRegion.height}%`,
                }}
              />
            ))}
            <span className="absolute left-[14%] top-[70%] h-px w-[50%] rotate-[-8deg] bg-plum/70" />
            <span className="absolute left-[56%] top-[63%] rounded-full bg-plum px-3 py-1 text-xs font-semibold text-white">
              1.82 mm
            </span>
          </div>
        )}
      </div>
    </section>
  );
}
