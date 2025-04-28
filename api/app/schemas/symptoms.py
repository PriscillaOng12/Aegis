from datetime import datetime
from pydantic import BaseModel, Field, conint, constr


class SymptomCreateRequest(BaseModel):
    pain: conint(ge=0, le=10) = Field(..., description="Pain level (0–10)")
    fatigue: conint(ge=0, le=10) = Field(..., description="Fatigue level (0–10)")
    nausea: conint(ge=0, le=10) = Field(..., description="Nausea level (0–10)")
    notes: constr(max_length=1024) = Field("", description="Free‑text notes")
    timestamp: datetime = Field(..., description="UTC timestamp of the symptom log")


class SymptomCreateResponse(BaseModel):
    id: str
    user_id: str
    created_at: datetime