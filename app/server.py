import typing as t
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.session import get_db
from app.schemas.task import TaskSchema
from app.schemas.solution import SolutionInputSchema
from app.schemas.user import UserSchema, UserInputSchema
from app.schemas.token import Token
from app import crud
from app.auth import get_current_user, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_password_hash
from logging import getLogger

logger = getLogger(__name__)

app = FastAPI()


@app.get("/tasks", response_model=list[TaskSchema], tags=["Task"])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    return await crud.task.get_tasks(db)


@app.get("/tasks/{task_id}", response_model=TaskSchema, tags=["Task"])
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.task.get_task(db, task_id)


@app.post("/tasks", response_model=TaskSchema, tags=["Task"])
async def add_task(task_data: TaskSchema, current_user: t.Annotated[UserSchema, Depends(get_current_user)],
                   db: AsyncSession = Depends(get_db)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can add tasks")
    return await crud.task.add_task(db, task_data, current_user)


@app.patch("/tasks/{task_id}", response_model=TaskSchema, tags=["Task"])
async def update_task(task_data: TaskSchema, task_id: int,
                      current_user: t.Annotated[UserSchema, Depends(get_current_user)],
                      db: AsyncSession = Depends(get_db)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can change tasks")
    return await crud.task.update_task(db, task_id, task_data, current_user)


@app.post("/tasks/{task_id}/add_solution", tags=["Task"])
async def add_solution(task_solution: SolutionInputSchema, task_id: int,
                       current_user: t.Annotated[UserSchema, Depends(get_current_user)],
                       db: AsyncSession = Depends(get_db)):
    return await crud.solution.validate_solution(db, task_id, task_solution, current_user)


@app.get("/tasks/{task_id}/solutions", tags=["Task"])
async def get_task_solutions(task_id: int, current_user: t.Annotated[UserSchema, Depends(get_current_user)],
                             db: AsyncSession = Depends(get_db)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can see solutions")
    return await crud.solution.get_task_solutions(db, task_id)


@app.post("/users/create_user", tags=["User"])
async def add_user(user_data: UserInputSchema, db: AsyncSession = Depends(get_db)):
    user = await crud.user.get_user(db, user_data.username)
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    user_data.password = get_password_hash(user_data.password)
    return await crud.user.add_user(db, user_data)


@app.get("/users/me", tags=["User"])
async def read_users_me(current_user: t.Annotated[UserSchema, Depends(get_current_user)]):
    return current_user


@app.post("/token", response_model=Token, tags=["Token"])
async def login_for_access_token(
        form_data: t.Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
