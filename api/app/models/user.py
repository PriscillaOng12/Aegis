from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: str = Column(String, primary_key=True)
    tenant_id: str = Column(String, index=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    auth_identities = relationship("AuthIdentity", back_populates="user")
    symptom_logs = relationship("SymptomLog", back_populates="user")
    wearable_snapshots = relationship("WearableSnapshot", back_populates="user")
    risk_scores = relationship("RiskScore", back_populates="user")
    interventions = relationship("Intervention", back_populates="user")