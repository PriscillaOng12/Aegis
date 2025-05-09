"""Router for risk scoring operations."""

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.jwt import verify_token
from ..services.db import get_session
from ..services.ml import get_risk
from ..schemas import RiskResponse, FeatureImpact
from ..models import RiskScore
import uuid
import json
import asyncio


router = APIRouter()


@router.get("/risk/latest", response_model=RiskResponse)
async def latest_risk(token_payload: dict = Depends(verify_token), session: AsyncSession = Depends(get_session)) -> RiskResponse:
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    result = await get_risk(user_id)
    # Persist risk score
    risk_id = str(uuid.uuid4())
    score = RiskScore(
        id=risk_id,
        user_id=user_id,
        risk_percentage=result["risk_percentage"],
        top_drivers=json.dumps(result["top_drivers"]),
        lead_time_hours=result.get("lead_time_hours"),
    )
    session.add(score)
    await session.commit()
    return RiskResponse(
        risk_percentage=result["risk_percentage"],
        top_drivers=[FeatureImpact(**d) for d in result["top_drivers"]],
        lead_time_hours=result.get("lead_time_hours"),
    )


@router.websocket("/risk/stream")
async def risk_stream(websocket: WebSocket):
    """WebSocket endpoint that streams risk updates every 10 seconds."""
    await websocket.accept(subprotocol="bearer")
    # In a real implementation we would verify the token from subprotocol header.
    user_id = "dev-user"
    try:
        while True:
            result = await get_risk(user_id)
            await websocket.send_json({
                "timestamp": f"{asyncio.get_event_loop().time()}",
                "risk_percentage": result["risk_percentage"],
            })
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        return