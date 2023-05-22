from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.solution import SolutionInputSchema
from app.schemas.user import UserSchema
from app.models.models import Solution
from app.crud.task import get_task
from app.crud.user import get_user
from app.crud.utils import create_container_if_not_exists, get_db_demo_connection, analyze_query

logger = getLogger(__name__)


async def validate_solution(db: AsyncSession, task_id: int, task_solution: SolutionInputSchema,
                            current_user: UserSchema) -> str:
    solution = Solution(query=task_solution.query)
    solution.user = await get_user(db, current_user.username)
    task = await get_task(db, task_id)
    solution.task = task
    await create_container_if_not_exists(current_user.username)
    solution_query = task_solution.query.lower()

    for keyword in set(task.excluded_keywords or []):
        if keyword in solution_query:
            solution.verdict = "Excluded keyword was used"
            db.add(task)
            await db.commit()
            return "Excluded keyword was used"

    for keyword in set(task.included_keywords or []):
        if keyword not in solution_query:
            solution.verdict = "Included keywords was not used"
            db.add(task)
            await db.commit()
            return "Included keywords was not used"

    conn = get_db_demo_connection(current_user.username)

    with conn:
        with conn.cursor() as cur:
            cur.execute(task.answer_query)
            ans_from_task = cur.fetchall()
            logger.info(f"Right answer: {ans_from_task}")
    conn.rollback()

    with conn:
        with conn.cursor() as cur:
            try:
                cur.execute(task_solution.query)
                ans_from_solution = cur.fetchall()
                logger.info(f"Solution answer: {ans_from_solution}")
            except Exception as e:
                solution.verdict = "Error"
                solution.verdict_description = str(e)
                db.add(task)
                await db.commit()
                return str(e)
    conn.rollback()

    if ans_from_task != ans_from_solution:
        solution.verdict = "Wrong answer"
        db.add(task)
        await db.commit()
        return "Wrong answer"

    rows, full_time = await analyze_query(task_solution.query, current_user.username)
    solution.rows_affected = rows
    solution.execution_time = full_time

    if rows > task.rows_affected or full_time * 0.7 > task.execution_time:
        solution.verdict = "Less effective than standard"
        db.add(task)
        await db.commit()
        return "Less effective than standard"

    for keyword in set(task.excluded_keywords_perf or []):
        if keyword in solution_query:
            solution.verdict = "Excluded 'performance' keyword was used"
            db.add(task)
            await db.commit()
            return "Excluded 'performance' keyword was used"

    for keyword in set(task.included_keywords_perf or []):
        if keyword not in solution_query:
            solution.verdict = "Included 'performance' keywords was not used"
            db.add(task)
            await db.commit()
            return "Included 'performance' keywords was not used"

    solution.verdict = "Right answer"
    db.add(task)
    await db.commit()
    return "Right answer"


async def get_task_solutions(db: AsyncSession, task_id: int):
    task = await get_task(db, task_id)
    return task.solutions
