from typing import TypedDict

from app.models.compliance import InspectionStatus, RuleResult
from app.models.inspection import Detection, ProductLabelData
from app.models.ocr import OCRWord


class InspectionState(TypedDict, total=False):
    inspection_id: str
    image_path: str
    marker_detected: bool
    marker_corners: list[list[float]]
    homography: list[list[float]] | None
    detections: list[Detection]
    ocr_results: list[OCRWord]
    measurements: dict[str, float | str | None]
    product_data: ProductLabelData
    rule_results: list[RuleResult]
    score: int
    status: InspectionStatus
    report_path: str
    evidence_hash: str
