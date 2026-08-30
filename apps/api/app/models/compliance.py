from enum import StrEnum

from pydantic import BaseModel


class RuleStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    NOT_VERIFIABLE = "NOT_VERIFIABLE"


class InspectionStatus(StrEnum):
    COMPLIANT = "COMPLIANT"
    REVIEW = "REVIEW"
    NON_COMPLIANT = "NON_COMPLIANT"


class RuleResult(BaseModel):
    rule_id: str
    name: str
    status: RuleStatus
    observed_value: str | None = None
    expected_value: str | None = None
    evidence_ids: list[str] = []
    message: str
    severity: str = "major"
