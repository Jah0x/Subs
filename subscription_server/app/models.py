from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy.sql import func
from enum import StrEnum
from .database import Base

class UIDStatus(StrEnum):
    free = "free"
    assigned = "assigned"
    suspended = "suspended"
    expired = "expired"

class UID(Base):
    __tablename__ = "uids"
    uid: Mapped[str] = mapped_column(String(36), primary_key=True)
    status: Mapped[str] = mapped_column(String(16), default=UIDStatus.free.value, index=True)
    assigned_user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    plan_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    expires_at: Mapped["DateTime | None"] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
