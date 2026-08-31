from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ExtractedProductData(BaseModel):
    mrp: float | None = None
    net_weight_value: float | None = None
    net_weight_unit: str | None = None
    manufacturer: str | None = None
    manufacturing_date: str | None = None
    expiry_date: str | None = None
    batch_number: str | None = None
    customer_care_phone: str | None = None
    banned_qualifiers: list[str] = []


class DetectionDoc(BaseModel):
    detection_id: str
    label: str
    confidence: float = Field(ge=0, le=1)
    bbox: list[float]
    obb: list[list[float]] | None = None


class OCRWordDoc(BaseModel):
    text: str
    confidence: float = Field(ge=0, le=1)
    bbox: list[list[float]]
    height_px: float = Field(ge=0)
    height_mm: float | None = None


class RuleResultDoc(BaseModel):
    rule_id: str
    name: str
    status: str
    observed_value: str | None = None
    expected_value: str | None = None
    evidence_ids: list[str] = []
    message: str
    severity: str = "major"


class EvidenceHashes(BaseModel):
    original_image_sha256: str | None = None
    result_json_sha256: str | None = None
    annotated_image_sha256: str | None = None
    report_pdf_sha256: str | None = None


class InspectionDocument(BaseModel):
    id: str = Field(alias="_id")
    product_name: str | None = None
    category: str | None = None
    status: str = "CREATED"
    score: int | None = None
    image_path: str | None = None
    evidence_hash: str | None = None
    evidence_hashes: EvidenceHashes = Field(default_factory=EvidenceHashes)
    hash_algorithm: str | None = "SHA-256"
    hashed_at: datetime | None = None
    pipeline_status: str | None = None
    marker_detected: bool = False
    homography: list[list[float]] | None = None
    detections: list[DetectionDoc] = []
    ocr_results: list[OCRWordDoc] = []
    measurements: dict[str, float | str | None] = {}
    product_data: ExtractedProductData | None = None
    rule_results: list[RuleResultDoc] = []
    image_path: str | None = None
    annotated_image_path: str | None = None
    report_path: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
