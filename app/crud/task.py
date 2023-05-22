import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Task
from app.schemas.task import TaskSchema
from app.crud.utils import update_attrs, analyze_query
from logging import getLogger

from app.schemas.user import UserSchema


logger = getLogger(__name__)


async def get_tasks(db: AsyncSession) -> list[Task]:
    return (await db.execute(sa.select(Task))).scalars().all()


async def get_task(db: AsyncSession, task_id: int) -> Task:
    return (await db.execute(sa.select(Task).filter(Task.id == task_id))).scalars().first()


async def add_task(db: AsyncSession, task_data: TaskSchema, current_user: UserSchema) -> Task:
    rows, full_time = await analyze_query(task_data.answer_query, current_user.username)
    task = Task(**task_data.dict(exclude={"id"}, exclude_unset=True), rows_affected=rows, execution_time=full_time)
    db.add(task)
    await db.commit()
    return task


async def update_task(db: AsyncSession, task_id: int, task_data: TaskSchema, current_user: UserSchema) -> Task:
    task = await get_task(db, task_id)
    update_attrs(task, **task_data.dict(exclude={"id"}, exclude_unset=True))
    if task_data.answer_query is not None:
        rows, full_time = await analyze_query(task_data.answer_query, current_user.username)
        update_attrs(task, rows_affected=rows, execution_time=full_time)
    await db.commit()
    return task
