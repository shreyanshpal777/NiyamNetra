import { apiDelay } from "./client";
import { mockInspections } from "../data/mockInspections";
import type { Inspection, NewInspectionInput, RuleStatus, InspectionStatus } from "../types/inspection";

let mockStore: Inspection[] = [...mockInspections];

function mapBackendStatus(status?: string): InspectionStatus {
  if (status === "COMPLIANT") return "PASS";
  if (status === "REVIEW") return "REVIEW";
  if (status === "NON_COMPLIANT") return "FAIL";
  return "NOT_VERIFIABLE";
}

function mapBackendRuleStatus(status?: string): RuleStatus {
  if (status === "PASS") return "PASS";
  if (status === "WARNING") return "WARNING";
  if (status === "FAIL") return "FAIL";
  return "NOT_VERIFIABLE";
}

function mapBackendInspection(doc: any): Inspection {
  const pd = doc.product_data || doc.extracted_data || {};
  return {
    id: doc.id || doc._id,
    productName: doc.product_name || pd.product_name || "Package Label",
    category: doc.category || pd.category || "General",
    date: doc.created_at
      ? new Intl.DateTimeFormat("en", { month: "short", day: "numeric", year: "numeric" }).format(new Date(doc.created_at))
      : new Intl.DateTimeFormat("en", { month: "short", day: "numeric", year: "numeric" }).format(new Date()),
    score: doc.score ?? 0,
    status: mapBackendStatus(doc.status),
    imageUrl: doc.annotated_image_path
      ? `/api/inspections/${doc.id}/annotated`
      : doc.image_path
      ? `/api/inspections/${doc.id}/image`
      : undefined,
    extractedData: {
      mrp: pd.mrp ? `₹${pd.mrp}` : "Not declared",
      netWeight: pd.net_weight_value ? `${pd.net_weight_value} ${pd.net_weight_unit || "g"}` : "Not declared",
      manufacturer: pd.manufacturer || "Not declared",
      batchNumber: pd.batch_number || "Not declared",
      category: doc.category || "General",
      packedOn: pd.manufacturing_date || "Not declared",
      customerCare: pd.customer_care_phone || "Not declared",
    },
    ocrWords: (doc.ocr_results || []).map((w: any, idx: number) => ({
      id: `w-${idx}`,
      text: w.text,
      confidence: w.confidence,
      box: {
        x: w.bbox?.[0]?.[0] || 0,
        y: w.bbox?.[0]?.[1] || 0,
        width: w.height_px || 20,
        height: w.height_px || 20,
      },
    })),
    ruleResults: (doc.rule_results || []).map((r: any, idx: number) => ({
      id: `r-${idx}`,
      ruleName: r.name || r.rule_name || "Rule Check",
      status: mapBackendRuleStatus(r.status),
      explanation: r.message || r.explanation || "",
      detectedText: r.observed_value || r.detected_text || "",
      confidence: 0.95,
      measuredHeight: r.measured_height ? `${r.measured_height} mm` : undefined,
      evidenceRegion: { x: 50, y: 50, width: 100, height: 40 },
    })),
  };
}

export async function createInspection(input: NewInspectionInput): Promise<Inspection> {
  try {
    const url = `/api/inspections?product_name=${encodeURIComponent(input.productName)}&category=${encodeURIComponent(input.category)}`;
    const res = await fetch(url, { method: "POST" });
    if (res.ok) {
      const data = await res.json();
      return mapBackendInspection(data);
    }
  } catch (err) {
    console.warn("Backend unavailable, using mock creation", err);
  }

  const nextNumber = mockStore.length + 1;
  const id = `INS-${String(nextNumber).padStart(3, "0")}`;
  const inspection: Inspection = {
    ...mockInspections[0],
    id,
    productName: input.productName || "Premium Wheat Flour",
    category: input.category || "Staple food",
    date: new Intl.DateTimeFormat("en", { month: "short", day: "numeric", year: "numeric" }).format(new Date()),
    score: 0,
    status: "NOT_VERIFIABLE",
  };
  mockStore = [inspection, ...mockStore];
  return apiDelay(inspection);
}

export async function getInspections(): Promise<Inspection[]> {
  try {
    const res = await fetch("/api/inspections");
    if (res.ok) {
      const data = await res.json();
      return data.map(mapBackendInspection);
    }
  } catch (err) {
    console.warn("Backend unavailable, using mock inspections list", err);
  }
  return apiDelay(mockStore);
}

export async function getInspection(id: string): Promise<Inspection> {
  try {
    const res = await fetch(`/api/inspections/${id}`);
    if (res.ok) {
      const data = await res.json();
      return mapBackendInspection(data);
    }
  } catch (err) {
    console.warn("Backend unavailable, returning local inspection", err);
  }
  const inspection = mockStore.find((item) => item.id === id) ?? mockInspections[0];
  return apiDelay(inspection);
}

export async function processInspection(id: string, imageBase64?: string): Promise<Inspection> {
  try {
    if (imageBase64 && imageBase64.startsWith("data:")) {
      const blob = await (await fetch(imageBase64)).blob();
      const formData = new FormData();
      formData.append("file", blob, `${id}.jpg`);
      await fetch(`/api/inspections/${id}/upload`, { method: "POST", body: formData });
    }

    const processRes = await fetch(`/api/inspections/${id}/process`, { method: "POST" });
    if (processRes.ok) {
      const data = await processRes.json();
      const result = mapBackendInspection(data);
      mockStore = mockStore.map((item) => (item.id === id ? result : item));
      return result;
    }
  } catch (err) {
    console.warn("Backend processing failed, using mock fallbacks", err);
  }

  const processed: Inspection = {
    ...mockInspections[0],
    id,
    imageUrl: imageBase64 || mockInspections[0].imageUrl,
    date: new Intl.DateTimeFormat("en", { month: "short", day: "numeric", year: "numeric" }).format(new Date()),
  };
  mockStore = mockStore.map((item) => (item.id === id ? processed : item));
  return apiDelay(processed, 600);
}

export async function getReport(id: string): Promise<{ id: string; url: string }> {
  return apiDelay({ id, url: `/api/inspections/${id}/report` });
}

