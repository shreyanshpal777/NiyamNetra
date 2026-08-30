export type InspectionStatus = "PASS" | "REVIEW" | "FAIL" | "NOT_VERIFIABLE";

export type RuleStatus = "PASS" | "WARNING" | "FAIL" | "NOT_VERIFIABLE";

export type ProcessingStage =
  | "Image"
  | "Calibration"
  | "Detection"
  | "OCR"
  | "Measurement"
  | "Extraction"
  | "Compliance"
  | "Report";

export interface OCRWord {
  id: string;
  text: string;
  confidence: number;
  box: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}

export interface ProductLabelData {
  mrp: string;
  netWeight: string;
  manufacturer: string;
  batchNumber: string;
  category: string;
  packedOn: string;
  customerCare: string;
}

export interface RuleResult {
  id: string;
  ruleName: string;
  status: RuleStatus;
  explanation: string;
  detectedText: string;
  confidence: number;
  measuredHeight?: string;
  evidenceRegion: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}

export interface Inspection {
  id: string;
  productName: string;
  category: string;
  date: string;
  score: number;
  status: InspectionStatus;
  imageUrl?: string;
  extractedData: ProductLabelData;
  ocrWords: OCRWord[];
  ruleResults: RuleResult[];
}

export interface NewInspectionInput {
  productName: string;
  category: string;
}
