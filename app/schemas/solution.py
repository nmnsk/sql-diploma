from app.schemas.base import BaseSchema, EmptyBaseSchema


class SolutionSchema(BaseSchema):
    query: str
    task_id: int
    user_id: int
    verdict: str
    verdict_description: str
    rows_affected: int
    execution_time: int


class SolutionInputSchema(EmptyBaseSchema):
    query: str
