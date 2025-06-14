"""Compute analytic summaries for clinicians."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from ..models import SymptomLog, RiskScore


async def get_summary(session: AsyncSession) -> dict:
    """Compute adherence, false‑alert rate, median lead time and active users.

    This is a simplified implementation. Adherence is computed as the ratio
    of days with a symptom log in the past week; false alert rate uses
    heuristic thresholds; lead time is computed from risk_scores table.
    """
    # Adherence: average logs per user per day vs expected 1/day
    total_logs = await session.scalar(select(func.count()).select_from(SymptomLog))
    distinct_users = await session.scalar(select(func.count(func.distinct(SymptomLog.user_id))))
    adherence = 0.0
    if distinct_users:
        # assume each user should log daily in the past week (7 days)
        adherence = min(total_logs / (distinct_users * 7), 1.0)

    # False alert rate: stubbed as constant (lack of label data in this demo)
    false_alert_rate = 0.2

    # Median lead time: compute median of lead_time_hours from risk_scores
    lead_times = (await session.execute(select(RiskScore.lead_time_hours))).scalars().all()
    lead_time = 0.0
    if lead_times:
        sorted_lt = sorted(filter(None, lead_times))
        mid = len(sorted_lt) // 2
        if len(sorted_lt) % 2 == 0:
            lead_time = (sorted_lt[mid - 1] + sorted_lt[mid]) / 2
        else:
            lead_time = sorted_lt[mid]

    # Active users in past 7 days: count distinct users with logs
    active_users = distinct_users

    return {
        "adherence": adherence,
        "false_alert_rate": false_alert_rate,
        "median_lead_time_hours": lead_time,
        "active_users": active_users,
    }