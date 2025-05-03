from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class WearableSnapshot(Base):
    __tablename__ = "wearable_snapshots"
    id: str = Column(String, primary_key=True)
    user_id: str = Column(String, ForeignKey("users.id"), nullable=False)
    source: str = Column(String, nullable=False)
    timestamp: datetime = Column(DateTime, nullable=False)
    hr: float = Column(Float)
    hrv: float = Column(Float)
    steps: float = Column(Float)
    sleep: float = Column(Float)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    consent: bool = Column(Boolean, default=True)

    user = relationship("User", back_populates="wearable_snapshots")