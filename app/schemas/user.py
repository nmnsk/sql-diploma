from app.schemas.base import BaseSchema, EmptyBaseSchema


class UserSchema(BaseSchema):
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    is_superuser: bool | None
    username: str | None
    password: str | None


class UserInputSchema(EmptyBaseSchema):
    first_name: str
    last_name: str
    patronymic: str | None
    username: str
    password: str
