from app.compliance.base import ComplianceRule
from app.models.compliance import RuleResult, RuleStatus
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord

class BatchNumberRule(ComplianceRule):
    rule_id = "FSSAI_TRACE_002"
    name = "Batch / Lot Number Traceability"
    severity = "major"
    penalty = 15

    def evaluate(self, product_data: ProductLabelData, ocr_results: list[OCRWord]) -> RuleResult:
        if product_data.batch_number:
            return RuleResult(
                rule_id=self.rule_id, name=self.name, status=RuleStatus.PASS,
                observed_value=product_data.batch_number, expected_value="Alphanumeric identifier",
                message="Batch number found, enabling traceability.",
                evidence_ids=[product_data.batch_number]
            )
            
        # Instead of an outright FAIL, we might issue a WARNING if we suspect it's cut off
        return RuleResult(
            rule_id=self.rule_id, name=self.name, status=RuleStatus.WARNING,
            observed_value="Not found", expected_value="Alphanumeric identifier",
            message="Batch number missing. Required for FSSAI recall procedures.",
            severity=self.severity
        )