import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { getInspection } from "../api/inspections";
import { LoadingState } from "../components/common/LoadingState";
import { InspectionMeta } from "../components/inspection/InspectionMeta";
import { PageContainer } from "../components/layout/PageContainer";
import { ComplianceCheck } from "../components/results/ComplianceCheck";
import { EvidenceImage } from "../components/results/EvidenceImage";
import { ExtractedInformation } from "../components/results/ExtractedInformation";
import { ResultHeader } from "../components/results/ResultHeader";

export function ResultPage() {
  const { id = "INS-001" } = useParams();
  const { data: inspection, isLoading } = useQuery({
    queryKey: ["inspection", id],
    queryFn: () => getInspection(id),
  });

  if (isLoading || !inspection) {
    return (
      <PageContainer>
        <LoadingState message="Opening inspection result" />
      </PageContainer>
    );
  }

  return (
    <PageContainer className="space-y-8">
      <ResultHeader inspection={inspection} />
      <InspectionMeta inspection={inspection} />
      <EvidenceImage inspection={inspection} />
      <div className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
        <ExtractedInformation data={inspection.extractedData} />
        <ComplianceCheck rules={inspection.ruleResults} />
      </div>
    </PageContainer>
  );
}
