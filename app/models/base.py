from uuid import UUID, uuid4
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime.datetime] = mapped_column(sa.DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(sa.DateTime(timezone=True), default=utcnow, onupdate=utcnow)