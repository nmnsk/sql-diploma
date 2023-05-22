from pydantic import BaseModel
from datetime import datetime, time


class EmptyBaseSchema(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True
        json_encoders = {
            time: lambda v: v.strftime("%H:%M"),
        }


class BaseSchema(EmptyBaseSchema):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None
