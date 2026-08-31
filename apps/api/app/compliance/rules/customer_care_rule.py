from app.compliance.base import ComplianceRule
from app.models.compliance import RuleResult, RuleStatus
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord

class CustomerCareRule(ComplianceRule):
    rule_id = "GRIEVANCE_001"
    name = "Consumer Care Details"
    severity = "minor"
    penalty = 10

    def evaluate(self, product_data: ProductLabelData, ocr_results: list[OCRWord]) -> RuleResult:
        if product_data.customer_care_phone:
            return RuleResult(
                rule_id=self.rule_id, name=self.name, status=RuleStatus.PASS,
                observed_value=product_data.customer_care_phone, expected_value="Phone number or Email",
                message="Consumer grievance contact is available.",
                evidence_ids=[product_data.customer_care_phone]
            )
            
        return RuleResult(
            rule_id=self.rule_id, name=self.name, status=RuleStatus.FAIL,
            observed_value="Not found", expected_value="Phone number or Email",
            message="No customer care contact details found.",
            severity=self.severity
        )