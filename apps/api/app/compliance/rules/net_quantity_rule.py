from app.compliance.base import ComplianceRule
from app.models.compliance import RuleResult, RuleStatus
from app.models.inspection import ProductLabelData
from app.models.ocr import OCRWord

class NetQuantityRule(ComplianceRule):
    rule_id = "METRO_QTY_001"
    name = "Standardized Net Quantity"
    severity = "major"
    penalty = 20
    
    # Valid SI units required by Legal Metrology
    VALID_UNITS = {"g", "kg", "mg", "ml", "l", "litre", "litres"}

    def evaluate(self, product_data: ProductLabelData, ocr_results: list[OCRWord]) -> RuleResult:
        if not product_data.net_weight_value:
            return RuleResult(
                rule_id=self.rule_id, name=self.name, status=RuleStatus.FAIL,
                observed_value="Not found", expected_value="Numeric value + SI Unit",
                message="Net quantity declaration is missing.", severity=self.severity
            )

        unit = str(product_data.net_weight_unit).lower().strip()
        observed = f"{product_data.net_weight_value} {unit}"

        if unit not in self.VALID_UNITS:
            return RuleResult(
                rule_id=self.rule_id, name=self.name, status=RuleStatus.FAIL,
                observed_value=observed, expected_value="Standard SI unit (g, kg, ml, L)",
                message=f"Non-standard unit '{unit}' used for net quantity.",
                severity=self.severity
            )

        return RuleResult(
            rule_id=self.rule_id, name=self.name, status=RuleStatus.PASS,
            observed_value=observed, expected_value="Numeric value + SI Unit",
            message="Net quantity correctly declared using standard units.",
            evidence_ids=[observed]
        )