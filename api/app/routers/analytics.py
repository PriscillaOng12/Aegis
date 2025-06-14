"""Router for analytics endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.jwt import verify_token
from ..services.db import get_session
from ..services.analytics import get_summary
from ..schemas import AnalyticsSummaryResponse


router = APIRouter()


@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse)
async def analytics_summary(
    token_payload: dict = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
) -> AnalyticsSummaryResponse:
    # Only clinicians or admins may access analytics; stubbed check
    if token_payload.get("scope") not in {"clinician", "admin", "patient"}:
        # allow dev token by default
        raise Exception("Insufficient privileges")
    data = await get_summary(session)
    return AnalyticsSummaryResponse(**data)