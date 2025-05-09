from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class RiskScore(Base):
    __tablename__ = "risk_scores"
    id: str = Column(String, primary_key=True)
    user_id: str = Column(String, ForeignKey("users.id"), nullable=False)
    risk_percentage: float = Column(Float, nullable=False)
    top_drivers: str = Column(String)  # JSON-encoded list of drivers
    lead_time_hours: float = Column(Float)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="risk_scores")