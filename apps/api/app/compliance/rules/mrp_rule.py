from app.compliance.base import ComplianceRule
from app.models.compliance import RuleResult, RuleStatus
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord

class MRPDeclarationRule(ComplianceRule):
    rule_id = "MRP_001"
    name = "Mandatory MRP Declaration"
    severity = "critical"
    penalty = 25

    def evaluate(self, product_data: ProductLabelData, ocr_results: list[OCRWord]) -> RuleResult:
        if product_data.mrp is not None:
            # Find the OCR word that gave us this MRP to use as evidence
            evidence_texts = [word.text for word in ocr_results if str(product_data.mrp) in word.text]
            
            return RuleResult(
                rule_id=self.rule_id,
                name=self.name,
                status=RuleStatus.PASS,
                observed_value=f"₹{product_data.mrp}",
                expected_value="Must be present",
                message="MRP clearly declared on the principal display panel.",
                evidence_ids=evidence_texts # The frontend uses this to highlight the image
            )
            
        return RuleResult(
            rule_id=self.rule_id,
            name=self.name,
            status=RuleStatus.FAIL,
            observed_value="Not found",
            expected_value="Must be present",
            message="No valid Maximum Retail Price (MRP) detected.",
            severity=self.severity
        )