"""Router for interventions (nudges)."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.jwt import verify_token
from ..services.db import get_session
from ..schemas import InterventionRequest, InterventionResponse
from ..services.interventions import trigger_intervention


router = APIRouter()


@router.post("/interventions/trigger", response_model=InterventionResponse, status_code=status.HTTP_202_ACCEPTED)
async def trigger_nudge(
    req: InterventionRequest,
    token_payload: dict = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
) -> InterventionResponse:
    # Only allow clinician or admin roles; stubbed check
    role = token_payload.get("scope", "patient")
    if role not in {"clinician", "admin", "patient"}:  # allow dev token
        raise Exception("Insufficient privileges")
    intervention_id = await trigger_intervention(
        session=session,
        user_id=req.user_id,
        template_id=req.template_id,
        scheduled_for=req.scheduled_for,
    )
    return InterventionResponse(intervention_id=intervention_id)