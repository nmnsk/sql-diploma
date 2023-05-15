import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskSchema, TaskSolution
from uuid import UUID
from app.crud.utils import update_attrs
import psycopg2
from logging import getLogger
from app.settings import settings


logger = getLogger(__name__)


async def get_tasks(db: AsyncSession) -> list[Task]:
    return (await db.execute(sa.select(Task))).scalars().all()


async def get_task(db: AsyncSession, task_id: UUID) -> Task:
    return (await db.execute(sa.select(Task).filter(Task.id == task_id))).scalars().first()


async def add_task(db: AsyncSession, task_data: TaskSchema) -> Task:
    task = Task(**task_data.dict(exclude={"id"}, exclude_unset=True))
    db.add(task)
    await db.commit()
    return task


async def update_task(db: AsyncSession, task_id: UUID, task_data: TaskSchema) -> Task:
    task = await get_task(db, task_id)
    update_attrs(task, **task_data.dict(exclude={"id"}, exclude_unset=True))
    await db.commit()
    return task


async def validate_solution(db: AsyncSession, task_id: UUID, task_solution: TaskSolution) -> str:
    task = await get_task(db, task_id)
    solution = task_solution.solution.lower()
    for keyword in set(task.excluded_keywords):
        if keyword in solution:
            return "Excluded keyword was used"
    for keyword in set(task.included_keywords):
        if keyword not in solution:
            return "Included keywords was not used"
    conn = psycopg2.connect(database=settings.DB_DEMO_DATABASE, user=settings.DB_DEMO_USER,
                            password=settings.DB_DEMO_PASSWORD, host=settings.DB_DEMO_HOST, port=5432)

    with conn.cursor() as cur:
        cur.execute(task.answer_query)
        ans_from_task = cur.fetchall()
        logger.info(f"Right answer: {ans_from_task}")
    with conn.cursor() as cur:
        cur.execute(task_solution.solution)
        ans_from_solution = cur.fetchall()
        logger.info(f"Solution answer: {ans_from_solution}")

    if ans_from_task != ans_from_solution:
        return "Wrong answer"

    return "Right answer"
