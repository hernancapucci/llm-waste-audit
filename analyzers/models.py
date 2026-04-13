from pydantic import BaseModel
from typing import List, Optional


class WasteDetection(BaseModel):
    waste_class: str
    confidence: float
    description: str
    potential_savings_percent: Optional[float] = None
    suggestion: str


class AuditResult(BaseModel):
    cacheability_score: float
    context_bloat_score: float
    flagged_wastes: List[WasteDetection]
    total_estimated_savings: str
    report: str
