import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Search } from "lucide-react";
import { getInspections } from "../api/inspections";
import { EmptyState } from "../components/common/EmptyState";
import { InspectionCard } from "../components/inspection/InspectionCard";
import { PageContainer } from "../components/layout/PageContainer";
import type { InspectionStatus } from "../types/inspection";

const statuses: Array<InspectionStatus | "ALL"> = ["ALL", "PASS", "REVIEW", "FAIL"];

export function HistoryPage() {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<InspectionStatus | "ALL">("ALL");
  const { data: inspections = [] } = useQuery({
    queryKey: ["inspections"],
    queryFn: getInspections,
  });

  const filtered = useMemo(
    () =>
      inspections.filter((inspection) => {
        const matchesSearch = `${inspection.id} ${inspection.productName}`
          .toLowerCase()
          .includes(search.toLowerCase());
        const matchesStatus = status === "ALL" || inspection.status === status;
        return matchesSearch && matchesStatus;
      }),
    [inspections, search, status],
  );

  return (
    <PageContainer>
      <section className="py-10 sm:py-16">
        <div className="grid gap-8 lg:grid-cols-[0.8fr_1fr] lg:items-end">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">Inspection history</p>
            <h1 className="display-heading mt-5 text-5xl font-semibold text-ink sm:text-7xl">
              Inspections
            </h1>
            <p className="mt-6 max-w-lg text-base leading-7 text-muted">
              Review previous inspection results and evidence.
            </p>
          </div>
          <div className="rounded-[2rem] bg-white p-4 sm:p-5">
            <div className="grid gap-3 sm:grid-cols-[1fr_auto]">
              <label className="relative">
                <Search className="absolute left-4 top-1/2 size-4 -translate-y-1/2 text-muted" />
                <input
                  className="h-11 w-full rounded-full border border-line bg-canvas pl-11 pr-4 text-sm"
                  onChange={(event) => setSearch(event.target.value)}
                  placeholder="Search inspection or product"
                  value={search}
                />
              </label>
              <div className="flex flex-wrap gap-2">
                {statuses.map((item) => (
                  <button
                    className={`rounded-full px-4 py-2 text-xs font-semibold transition ${
                      status === item ? "bg-plum text-white" : "bg-canvas text-muted hover:bg-lavender"
                    }`}
                    key={item}
                    onClick={() => setStatus(item)}
                    type="button"
                  >
                    {item === "ALL" ? "All" : item}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="mt-10 grid gap-3">
          {filtered.length > 0 ? (
            filtered.map((inspection) => <InspectionCard inspection={inspection} key={inspection.id} />)
          ) : (
            <EmptyState message="No inspections match these filters." />
          )}
        </div>
      </section>
    </PageContainer>
  );
}
