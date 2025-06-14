from datetime import datetime
from pydantic import BaseModel, Field


class InterventionRequest(BaseModel):
    template_id: str = Field(..., description="Identifier of the nudge template")
    user_id: str = Field(..., description="Target user ID")
    scheduled_for: datetime = Field(..., description="When to send the nudge (UTC)")


class InterventionResponse(BaseModel):
    intervention_id: str