from app.schemas.base import BaseSchema, EmptyBaseSchema


class TaskSchema(BaseSchema):
    name: str | None
    answer_query: str | None
    description: str | None
    included_keywords: list[str] | None
    excluded_keywords: list[str] | None
