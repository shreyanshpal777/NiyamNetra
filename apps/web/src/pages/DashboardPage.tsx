import { useQuery } from "@tanstack/react-query";
import { ArrowUpRight, BadgeCheck, Boxes, Ruler, ScanText, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";
import { getInspections } from "../api/inspections";
import { ActivitySection } from "../components/dashboard/ActivitySection";
import { ComplianceOverview } from "../components/dashboard/ComplianceOverview";
import { FeatureCard } from "../components/dashboard/FeatureCard";
import { RecentInspectionList } from "../components/dashboard/RecentInspectionList";
import { InspectionHeroVisual } from "../components/hero/InspectionHeroVisual";
import { PageContainer } from "../components/layout/PageContainer";
import { Button } from "../components/ui/button";

export function DashboardPage() {
  const { data: inspections = [] } = useQuery({
    queryKey: ["inspections"],
    queryFn: getInspections,
  });

  return (
    <PageContainer className="space-y-20">
      <section className="grid gap-8 pt-6">
        <div className="mx-auto max-w-4xl text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-muted">
            AI-powered label inspection
          </p>
          <h1 className="display-heading mt-5 text-5xl font-semibold text-ink sm:text-7xl lg:text-8xl">
            Inspect every label with confidence.
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-base leading-7 text-muted">
            Capture a package label and automatically analyze declarations, measurements and compliance evidence.
          </p>
          <div className="mt-7 flex flex-wrap justify-center gap-3">
            <Button asChild>
              <Link to="/inspection/new">Start Inspection</Link>
            </Button>
            <Button asChild variant="secondary">
              <Link to="/inspections">View Inspections</Link>
            </Button>
          </div>
        </div>
        <InspectionHeroVisual />
      </section>

      <section className="grid gap-8 lg:grid-cols-[0.9fr_1fr] lg:items-start" id="checks">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">
            What does Inspector AI check?
          </p>
          <h2 className="display-heading mt-5 max-w-xl text-5xl font-semibold text-ink sm:text-6xl">
            Label evidence, measured and interpreted.
          </h2>
        </div>
        <div className="space-y-6">
          <p className="max-w-xl text-lg leading-8 text-muted">
            The inspection looks for mandatory declarations, MRP, quantity, typography, qualifiers and the visual proof behind every decision.
          </p>
          <ComplianceOverview />
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.25fr_0.85fr_0.85fr]">
        <FeatureCard
          className="lg:min-h-72"
          description="ArUco calibration lets the system convert image measurements into real-world dimensions."
          icon={<Ruler className="size-5" />}
          title="Measure, not just detect."
        />
        <FeatureCard
          description="PaddleOCR extracts text and its exact location from the package label."
          icon={<ScanText className="size-5" />}
          title="Read what matters."
          variant="dark"
        />
        <FeatureCard
          description="Every result connects the compliance decision to visual and textual evidence."
          icon={<ShieldCheck className="size-5" />}
          title="Evidence-backed decisions."
        />
      </section>

      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="rounded-[2rem] bg-plum p-8 text-white">
          <BadgeCheck className="size-8" />
          <h2 className="mt-14 max-w-sm text-4xl font-semibold leading-tight">
            From camera to compliance report.
          </h2>
          <p className="mt-5 max-w-md text-sm leading-6 text-white/65">
            Camera input moves through OpenCV, YOLO OBB, OCR, measurement, LLM extraction and deterministic rules before the PDF report is ready.
          </p>
          <Button asChild className="mt-7 bg-white text-plum hover:bg-lavender" size="sm">
            <Link to="/inspection/new">
              New Inspection
              <ArrowUpRight className="size-4" />
            </Link>
          </Button>
        </div>
        <div className="rounded-[2rem] bg-lavender p-8">
          <Boxes className="size-8 text-plum" />
          <div className="mt-14 grid grid-cols-2 gap-3 text-sm text-plum sm:grid-cols-4">
            {["Camera", "FastAPI", "OpenCV", "YOLO11", "PaddleOCR", "Measure", "Rules", "PDF"].map(
              (item) => (
                <span className="rounded-full bg-white px-4 py-3 text-center font-semibold" key={item}>
                  {item}
                </span>
              ),
            )}
          </div>
        </div>
      </section>

      <ActivitySection />
      <RecentInspectionList inspections={inspections.slice(0, 3)} />
    </PageContainer>
  );
}
