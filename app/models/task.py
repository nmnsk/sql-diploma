import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from app.models.base import Base


class Task(Base):
    __tablename__ = "task"

    name: Mapped[str] = mapped_column(sa.String(255))
    answer_query: Mapped[str] = mapped_column(sa.Text)
    description: Mapped[str] = mapped_column(sa.Text)
    included_keywords: Mapped[list[str]] = mapped_column(ARRAY(sa.String))
    excluded_keywords: Mapped[list[str]] = mapped_column(ARRAY(sa.String))
