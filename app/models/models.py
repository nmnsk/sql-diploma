import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from app.models.base import Base


class Task(Base):
    __tablename__ = "task"

    name: Mapped[str] = mapped_column(sa.String(255))
    answer_query: Mapped[str] = mapped_column(sa.Text)
    check_query: Mapped[str | None] = mapped_column(sa.Text)
    description: Mapped[str] = mapped_column(sa.Text)
    included_keywords: Mapped[list[str] | None] = mapped_column(ARRAY(sa.String))
    excluded_keywords: Mapped[list[str] | None] = mapped_column(ARRAY(sa.String))
    included_keywords_perf: Mapped[list[str] | None] = mapped_column(ARRAY(sa.String))
    excluded_keywords_perf: Mapped[list[str] | None] = mapped_column(ARRAY(sa.String))
    rows_affected: Mapped[int | None]
    execution_time: Mapped[float | None]
    send_hint: Mapped[bool] = mapped_column(default=False)

    solutions: Mapped[list["Solution"]] = relationship("Solution", back_populates="task", lazy="selectin")


class User(Base):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(sa.String(255))
    last_name: Mapped[str] = mapped_column(sa.String(255))
    patronymic: Mapped[str | None]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    username: Mapped[str] = mapped_column(sa.String(255), unique=True)
    password: Mapped[str] = mapped_column(sa.String(255))

    solutions: Mapped[list["Solution"]] = relationship("Solution", back_populates="user", lazy="selectin")


class Solution(Base):
    __tablename__ = "solution"

    query: Mapped[str] = mapped_column(sa.Text)
    task_id: Mapped[int] = mapped_column(sa.ForeignKey("task.id"))
    task: Mapped["Task"] = relationship("Task", back_populates="solutions", lazy="selectin")
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="solutions", lazy="selectin")
    verdict: Mapped[str] = mapped_column(sa.String(255))
    verdict_description: Mapped[str | None] = mapped_column(sa.Text)
    rows_affected: Mapped[int | None]
    execution_time: Mapped[float | None]
