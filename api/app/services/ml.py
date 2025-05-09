"""Client for the ML service used by the API."""

import os
import random
from typing import Any, Dict, List

import httpx


ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://localhost:8080")


async def get_risk(user_id: str) -> Dict[str, Any]:
    """Return the latest risk score for a user by calling the ML service.

    In this stub implementation, we return random values. In production, this
    function calls the TorchServe model server and passes the necessary
    features.
    """
    # Example of calling remote service (commented out)
    # async with httpx.AsyncClient() as client:
    #     resp = await client.post(f"{ML_SERVICE_URL}/predictions/aegis_model", json={"user_id": user_id})
    #     resp.raise_for_status()
    #     return resp.json()
    # For demonstration, produce deterministic pseudo‑random output based on user_id
    random.seed(hash(user_id) % 10000)
    risk_percentage = round(random.random(), 2)
    drivers = [
        {"feature": "sleep_efficiency_mean_7d", "impact": round(random.random() * 0.3, 2)},
        {"feature": "pain", "impact": round(random.random() * 0.3, 2)},
        {"feature": "hrv_rmssd_mean_3d", "impact": round(random.random() * 0.3, 2)},
    ]
    lead_time_hours = round(random.uniform(8, 24), 1)
    return {
        "risk_percentage": risk_percentage,
        "top_drivers": drivers,
        "lead_time_hours": lead_time_hours,
    }