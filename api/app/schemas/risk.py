from pydantic import BaseModel
from typing import List


class FeatureImpact(BaseModel):
    feature: str
    impact: float


class RiskResponse(BaseModel):
    risk_percentage: float
    top_drivers: List[FeatureImpact]
    lead_time_hours: float | None = None