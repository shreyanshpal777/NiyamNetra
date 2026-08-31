from app.models.compliance import InspectionStatus, RuleResult
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord
from app.compliance.rules.mrp_rule import MRPDeclarationRule
from app.compliance.rules.expiry_date_rule import ExpiryDateRule
from app.compliance.rules.net_quantity_rule import NetQuantityRule
from app.compliance.rules.batch_number_rule import BatchNumberRule
from app.compliance.rules.customer_care_rule import CustomerCareRule

class RuleEngine:
    def __init__(self):
        # Register all active rules here
        self.rules = [
            MRPDeclarationRule(),
            ExpiryDateRule(),
            NetQuantityRule(),
            BatchNumberRule(),
            CustomerCareRule()
        ]

    def evaluate(self, product_data: ProductLabelData, ocr_results: list[OCRWord]) -> tuple[list[RuleResult], int, InspectionStatus]:
        results = []
        score = 100

        for rule in self.rules:
            result = rule.evaluate(product_data, ocr_results)
            results.append(result)

            # Deduct points based on failure severity
            if result.status == "FAIL":
                score -= rule.penalty
            elif result.status == "WARNING":
                score -= (rule.penalty // 2)

        # Floor the score at 0
        score = max(0, score)

        if score >= 90:
            status = InspectionStatus.COMPLIANT
        elif score >= 70:
            status = InspectionStatus.REVIEW
        else:
            status = InspectionStatus.NON_COMPLIANT

        return results, score, status

# Instantiate a global engine to be used by your LangGraph nodes
compliance_engine = RuleEngine()