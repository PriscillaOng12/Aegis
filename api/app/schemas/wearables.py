from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class WearableSnapshotIn(BaseModel):
    timestamp: datetime = Field(..., description="UTC timestamp of the snapshot")
    hr: float | None = Field(None, description="Heart rate in bpm")
    hrv: float | None = Field(None, description="Heart rate variability (RMSSD proxy)")
    steps: float | None = Field(None, description="Number of steps in the interval")
    sleep: float | None = Field(None, description="Sleep minutes in the interval")


class WearablesSyncRequest(BaseModel):
    source: str = Field(..., description="Data source name (e.g., apple_health)")
    snapshots: List[WearableSnapshotIn]


class WearablesSyncResponse(BaseModel):
    ingested: int