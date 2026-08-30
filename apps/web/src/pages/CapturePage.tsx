import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { CameraPreview } from "../components/camera/CameraPreview";
import { CameraStatus } from "../components/camera/CameraStatus";
import { PageContainer } from "../components/layout/PageContainer";
import { useInspectionStore } from "../store/inspectionStore";

export function CapturePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { setCurrentInspection } = useInspectionStore();

  useEffect(() => {
    if (id) setCurrentInspection(id);
  }, [id, setCurrentInspection]);

  return (
    <PageContainer>
      <section className="mx-auto max-w-5xl py-10 sm:py-14">
        <div className="text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">Camera capture</p>
          <h1 className="display-heading mt-5 text-5xl font-semibold text-ink sm:text-7xl">
            Align the label.
          </h1>
          <p className="mx-auto mt-6 max-w-xl text-base leading-7 text-muted">
            Align the label and reference marker inside the frame.
          </p>
        </div>
        <div className="mt-10">
          <CameraPreview onAnalyze={() => navigate(`/inspection/${id ?? "INS-001"}/processing`)} />
        </div>
        <div className="mt-6">
          <CameraStatus />
        </div>
      </section>
    </PageContainer>
  );
}
