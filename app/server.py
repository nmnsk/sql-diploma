from uuid import UUID

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.session import get_db
from app.schemas.task import TaskSchema, TaskSolution
from app import crud
from logging import getLogger


logger = getLogger(__name__)


app = FastAPI()


@app.get("/tasks", response_model=list[TaskSchema], tags=["Task"])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    return await crud.task.get_tasks(db)


@app.get("/tasks/{task_id}", response_model=TaskSchema, tags=["Task"])
async def get_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    return await crud.task.get_task(db, task_id)


@app.post("/tasks", response_model=TaskSchema, tags=["Task"])
async def add_task(task_data: TaskSchema, db: AsyncSession = Depends(get_db)):
    return await crud.task.add_task(db, task_data)


@app.patch("/tasks/{task_id}", response_model=TaskSchema, tags=["Task"])
async def update_task(task_data: TaskSchema, task_id: UUID, db: AsyncSession = Depends(get_db)):
    return await crud.task.update_task(db, task_id, task_data)


@app.post("/tasks/{task_id}/add_solution", tags=["Task"])
async def add_solution(task_solution: TaskSolution, task_id: UUID, db: AsyncSession = Depends(get_db)):
    return await crud.task.validate_solution(db, task_id, task_solution)
