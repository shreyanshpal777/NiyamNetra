from abc import ABC, abstractmethod
from typing import List
from app.models.compliance import RuleResult
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord

class ComplianceRule(ABC):
    """
    Abstract base class for all product label compliance rules.
    """
    rule_id: str
    name: str
    severity: str
    penalty: int

    @abstractmethod
    def evaluate(self, product_data: ProductLabelData, ocr_results: List[OCRWord]) -> RuleResult:
        """
        Evaluate the rule against the extracted product data and OCR results.
        
        Args:
            product_data: The structured data extracted by the LLM.
            ocr_results: The raw list of OCR words and bounding boxes.
            
        Returns:
            RuleResult: The outcome of the rule evaluation.
        """
        pass
