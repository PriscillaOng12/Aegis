from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class SymptomLog(Base):
    __tablename__ = "symptom_logs"
    id: str = Column(String, primary_key=True)
    user_id: str = Column(String, ForeignKey("users.id"), nullable=False)
    pain: int = Column(Integer, default=0)
    fatigue: int = Column(Integer, default=0)
    nausea: int = Column(Integer, default=0)
    notes: str = Column(String, default="")
    timestamp: datetime = Column(DateTime, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    consent: bool = Column(Boolean, default=True)

    user = relationship("User", back_populates="symptom_logs")