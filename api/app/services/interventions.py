"""Service logic for interventions/nudges."""

import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Intervention


async def trigger_intervention(session: AsyncSession, user_id: str, template_id: str, scheduled_for: datetime) -> str:
    intervention_id = str(uuid.uuid4())
    intervention = Intervention(
        id=intervention_id,
        user_id=user_id,
        template_id=template_id,
        scheduled_for=scheduled_for,
    )
    session.add(intervention)
    await session.commit()
    # TODO: publish message to Pub/Sub or push notification service
    return intervention_id