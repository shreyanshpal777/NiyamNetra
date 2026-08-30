import { Check, Circle } from "lucide-react";
import { processingStages } from "../../data/mockInspections";
import { cn } from "../../lib/utils";
import type { ProcessingStage } from "../../types/inspection";

interface PipelineProgressProps {
  currentStage: ProcessingStage;
}

const stageCopy: Record<ProcessingStage, string> = {
  Image: "Image captured",
  Calibration: "Reference marker detected",
  Detection: "Package regions located",
  OCR: "Reading label",
  Measurement: "Measuring text",
  Extraction: "Extracting declarations",
  Compliance: "Evaluating compliance",
  Report: "Report prepared",
};

export function PipelineProgress({ currentStage }: PipelineProgressProps) {
  const currentIndex = processingStages.indexOf(currentStage);

  return (
    <div className="mx-auto max-w-2xl rounded-[2rem] bg-white p-6 shadow-sm sm:p-8">
      <ol className="grid gap-4">
        {processingStages.map((stage, index) => {
          const complete = index < currentIndex;
          const active = index === currentIndex;
          return (
            <li className="flex items-center gap-4" key={stage}>
              <span
                className={cn(
                  "flex size-8 items-center justify-center rounded-full ring-1",
                  complete && "bg-plum text-white ring-plum",
                  active && "bg-lavender text-plum ring-lavender-deep",
                  !complete && !active && "bg-canvas text-muted ring-line",
                )}
              >
                {complete ? <Check className="size-4" /> : <Circle className="size-3 fill-current" />}
              </span>
              <div>
                <p className={cn("text-sm font-semibold", active ? "text-ink" : "text-muted")}>
                  {stageCopy[stage]}
                </p>
                <p className="text-xs text-muted">{stage}</p>
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
