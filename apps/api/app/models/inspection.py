from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.models.compliance import InspectionStatus, RuleResult
from app.models.ocr import OCRWord


class ProductLabelData(BaseModel):
    product_name: str | None = None
    mrp: float | None = None
    net_weight_value: float | None = None
    net_weight_unit: str | None = None
    manufacturer: str | None = None
    manufacturing_date: str | None = None
    expiry_date: str | None = None
    batch_number: str | None = None
    customer_care_phone: str | None = None
    banned_qualifiers: list[str] = []


class Detection(BaseModel):
    detection_id: str
    label: str
    confidence: float = Field(ge=0, le=1)
    bbox: list[float]
    obb: list[list[float]] | None = None


class InspectionCreate(BaseModel):
    product_name: str | None = None
    category: str | None = None


class InspectionRecord(BaseModel):
    inspection_id: str
    product_name: str | None = None
    category: str | None = None
    image_path: str | None = None
    marker_detected: bool = False
    homography: list[list[float]] | None = None
    detections: list[Detection] = []
    ocr_results: list[OCRWord] = []
    measurements: dict[str, float | str | None] = {}
    product_data: ProductLabelData | None = None
    rule_results: list[RuleResult] = []
    score: int = 0
    status: InspectionStatus | None = None
    report_path: str | None = None
    evidence_hash: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InspectionCreateResponse(BaseModel):
    inspection_id: str


class InspectionListResponse(BaseModel):
    inspections: list[InspectionRecord]
