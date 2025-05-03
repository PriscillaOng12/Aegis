"""Router for wearable data ingestion."""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.jwt import verify_token
from ..services.db import get_session
from ..schemas import WearablesSyncRequest, WearablesSyncResponse
from ..models import WearableSnapshot, User


router = APIRouter()


@router.post("/wearables/sync", response_model=WearablesSyncResponse, status_code=status.HTTP_202_ACCEPTED)
async def sync_wearables(
    payload: WearablesSyncRequest,
    token_payload: dict = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
) -> WearablesSyncResponse:
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    user = await session.get(User, user_id)
    if user is None:
        user = User(id=user_id, tenant_id="default")
        session.add(user)
        await session.commit()
    for snap in payload.snapshots:
        snapshot = WearableSnapshot(
            id=str(uuid.uuid4()),
            user_id=user_id,
            source=payload.source,
            timestamp=snap.timestamp,
            hr=snap.hr,
            hrv=snap.hrv,
            steps=snap.steps,
            sleep=snap.sleep,
        )
        session.add(snapshot)
    await session.commit()
    return WearablesSyncResponse(ingested=len(payload.snapshots))