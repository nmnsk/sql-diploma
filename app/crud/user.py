import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User

from app.schemas.user import UserInputSchema


async def get_users(db: AsyncSession) -> list[User]:
    return (await db.execute(sa.select(User))).scalars().all()


async def get_user(db: AsyncSession, username: str) -> User:
    return (await db.execute(sa.select(User).filter(User.username == username))).scalars().first()


async def add_user(db: AsyncSession, user_data: UserInputSchema) -> User:
    user = User(**user_data.dict(exclude={"id", "is_superuser"}, exclude_unset=True))
    db.add(user)
    await db.commit()
    return user
