import asyncio
import os
import pytest
from httpx import AsyncClient

from ..main import create_app

# Configure test database (SQLite in memory)
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

app = create_app()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_token_exchange():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        resp = await ac.post("/v1/auth/exchange", json={"auth_code": "code", "code_verifier": "verifier"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["access_token"] == "dev-token"


@pytest.mark.asyncio
async def test_symptom_log_and_risk():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # create symptom log
        payload = {
            "pain": 4,
            "fatigue": 2,
            "nausea": 1,
            "notes": "feeling tired",
            "timestamp": "2025-08-10T00:00:00Z",
        }
        resp = await ac.post("/v1/symptoms", json=payload, headers={"Authorization": "Bearer dev-token"})
        assert resp.status_code == 201
        # fetch risk
        resp = await ac.get("/v1/risk/latest", headers={"Authorization": "Bearer dev-token"})
        assert resp.status_code == 200
        data = resp.json()
        assert 0.0 <= data["risk_percentage"] <= 1.0
        assert isinstance(data["top_drivers"], list)