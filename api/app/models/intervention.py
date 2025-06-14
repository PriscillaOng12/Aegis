from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Intervention(Base):
    __tablename__ = "interventions"
    id: str = Column(String, primary_key=True)
    user_id: str = Column(String, ForeignKey("users.id"), nullable=False)
    template_id: str = Column(String, nullable=False)
    scheduled_for: datetime = Column(DateTime, nullable=False)
    sent_at: datetime | None = Column(DateTime)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interventions")