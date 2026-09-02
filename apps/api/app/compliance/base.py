from abc import ABC, abstractmethod
from app.models.compliance import RuleResult
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord


class ComplianceRule(ABC):
    rule_id: str = ""
    name: str = ""
    severity: str = "major"
    penalty: int = 10

    @abstractmethod
    def evaluate(self, product_data: ProductLabelData, ocr_results: list[OCRWord]) -> RuleResult:
        pass
