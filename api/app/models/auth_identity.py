from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class AuthIdentity(Base):
    __tablename__ = "auth_identities"
    id: str = Column(String, primary_key=True)
    user_id: str = Column(String, ForeignKey("users.id"), nullable=False)
    provider: str = Column(String, nullable=False)
    subject: str = Column(String, nullable=False, unique=True)

    user = relationship("User", back_populates="auth_identities")