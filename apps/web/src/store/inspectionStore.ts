import { create } from "zustand";
import type { ProcessingStage } from "../types/inspection";

interface InspectionWorkflowState {
  currentInspectionId?: string;
  capturedImage?: string;
  cameraPermission: "idle" | "granted" | "denied";
  processingStage: ProcessingStage;
  selectedEvidenceId?: string;
  setCurrentInspection: (id: string) => void;
  setCapturedImage: (image?: string) => void;
  setCameraPermission: (permission: "idle" | "granted" | "denied") => void;
  setProcessingStage: (stage: ProcessingStage) => void;
  setSelectedEvidenceId: (id?: string) => void;
  resetWorkflow: () => void;
}

export const useInspectionStore = create<InspectionWorkflowState>((set) => ({
  cameraPermission: "idle",
  processingStage: "Image",
  setCurrentInspection: (id) => set({ currentInspectionId: id }),
  setCapturedImage: (image) => set({ capturedImage: image }),
  setCameraPermission: (cameraPermission) => set({ cameraPermission }),
  setProcessingStage: (processingStage) => set({ processingStage }),
  setSelectedEvidenceId: (selectedEvidenceId) => set({ selectedEvidenceId }),
  resetWorkflow: () =>
    set({
      capturedImage: undefined,
      cameraPermission: "idle",
      processingStage: "Image",
      selectedEvidenceId: undefined,
    }),
}));
