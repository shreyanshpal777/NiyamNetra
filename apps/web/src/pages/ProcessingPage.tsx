import { useEffect, useRef } from "react";
import { useMutation } from "@tanstack/react-query";
import { useNavigate, useParams } from "react-router-dom";
import { processInspection } from "../api/inspections";
import { processingStages } from "../data/mockInspections";
import { PageContainer } from "../components/layout/PageContainer";
import { PipelineProgress } from "../components/inspection/PipelineProgress";
import { useInspectionStore } from "../store/inspectionStore";

export function ProcessingPage() {
  const { id = "INS-001" } = useParams();
  const navigate = useNavigate();
  const mutationStarted = useRef(false);
  const { capturedImage, processingStage, setProcessingStage } = useInspectionStore();

  const { mutate } = useMutation({
    mutationFn: () => processInspection(id, capturedImage),
    onSuccess: () => navigate(`/inspection/${id}`),
  });

  useEffect(() => {
    let index = 0;
    setProcessingStage(processingStages[index]);
    const interval = window.setInterval(() => {
      index += 1;
      if (index < processingStages.length) {
        setProcessingStage(processingStages[index]);
      } else {
        window.clearInterval(interval);
        if (!mutationStarted.current) {
          mutationStarted.current = true;
          mutate();
        }
      }
    }, 620);

    return () => window.clearInterval(interval);
  }, [mutate, setProcessingStage]);

  return (
    <PageContainer>
      <section className="mx-auto max-w-4xl py-12 text-center sm:py-20">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">Processing</p>
        <h1 className="display-heading mt-5 text-5xl font-semibold text-ink sm:text-7xl">
          Analyzing your inspection
        </h1>
        <p className="mx-auto mt-6 max-w-xl text-base leading-7 text-muted">
          Detecting, reading and measuring the label.
        </p>
        <div className="mt-12 text-left">
          <PipelineProgress currentStage={processingStage} />
        </div>
      </section>
    </PageContainer>
  );
}
