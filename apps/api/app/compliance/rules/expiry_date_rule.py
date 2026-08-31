from app.compliance.base import ComplianceRule
from app.models.compliance import RuleResult, RuleStatus
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord

class ExpiryDateRule(ComplianceRule):
    rule_id = "FSSAI_DATE_001"
    name = "Mandatory Expiry / Best Before Date"
    severity = "critical"
    penalty = 30  # High penalty, major safety violation

    def evaluate(self, product_data: ProductLabelData, ocr_results: list[OCRWord]) -> RuleResult:
        if product_data.expiry_date:
            return RuleResult(
                rule_id=self.rule_id,
                name=self.name,
                status=RuleStatus.PASS,
                observed_value=product_data.expiry_date,
                expected_value="Date format (DD/MM/YY or MM/YY)",
                message="Expiry/Best Before date is clearly declared.",
                evidence_ids=[product_data.expiry_date]
            )
            
        return RuleResult(
            rule_id=self.rule_id,
            name=self.name,
            status=RuleStatus.FAIL,
            observed_value="Not found",
            expected_value="Must declare Expiry Date or Best Before",
            message="Critical FSSAI violation: No expiration marking detected.",
            severity=self.severity
        )