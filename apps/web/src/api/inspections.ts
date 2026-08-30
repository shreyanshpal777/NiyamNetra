import { apiDelay } from "./client";
import { mockInspections } from "../data/mockInspections";
import type { Inspection, NewInspectionInput } from "../types/inspection";

let inspections: Inspection[] = [...mockInspections];

function nextInspectionId() {
  const nextNumber = inspections.length + 1;
  return `INS-${String(nextNumber).padStart(3, "0")}`;
}

export async function createInspection(input: NewInspectionInput): Promise<Inspection> {
  const inspection: Inspection = {
    ...mockInspections[0],
    id: nextInspectionId(),
    productName: input.productName || "Untitled Package",
    category: input.category || "Package label",
    date: new Intl.DateTimeFormat("en", {
      month: "short",
      day: "numeric",
      year: "numeric",
    }).format(new Date()),
    score: 0,
    status: "NOT_VERIFIABLE",
  };

  inspections = [inspection, ...inspections];
  return apiDelay(inspection);
}

export async function getInspections(): Promise<Inspection[]> {
  return apiDelay(inspections);
}

export async function getInspection(id: string): Promise<Inspection> {
  const inspection = inspections.find((item) => item.id === id) ?? mockInspections[0];
  return apiDelay(inspection);
}

export async function processInspection(id: string, image?: string): Promise<Inspection> {
  const processed: Inspection = {
    ...mockInspections[0],
    id,
    imageUrl: image,
    date: new Intl.DateTimeFormat("en", {
      month: "short",
      day: "numeric",
      year: "numeric",
    }).format(new Date()),
  };

  inspections = inspections.map((item) => (item.id === id ? processed : item));
  if (!inspections.some((item) => item.id === id)) {
    inspections = [processed, ...inspections];
  }

  return apiDelay(processed, 600);
}

export async function getReport(id: string): Promise<{ id: string; url: string }> {
  return apiDelay({ id, url: `/reports/${id}.pdf` });
}
