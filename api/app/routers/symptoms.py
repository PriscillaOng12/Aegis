"""Router for symptom logging."""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from ..schemas import SymptomCreateRequest, SymptomCreateResponse
from ..services.db import get_session
from ..auth.jwt import verify_token
from ..models import SymptomLog, User


router = APIRouter()


@router.post("/symptoms", response_model=SymptomCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_symptom(
    payload: SymptomCreateRequest,
    token_payload: dict = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
) -> SymptomCreateResponse:
    """Create a new symptom log for the authenticated user."""
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    # Ensure user exists or create stub user
    user = await session.get(User, user_id)
    if user is None:
        user = User(id=user_id, tenant_id="default")
        session.add(user)
        await session.commit()
    log_id = str(uuid.uuid4())
    log = SymptomLog(
        id=log_id,
        user_id=user_id,
        pain=payload.pain,
        fatigue=payload.fatigue,
        nausea=payload.nausea,
        notes=payload.notes,
        timestamp=payload.timestamp,
    )
    session.add(log)
    await session.commit()
    return SymptomCreateResponse(id=log_id, user_id=user_id, created_at=log.created_at)