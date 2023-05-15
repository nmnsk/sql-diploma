from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.settings import settings

engine = create_async_engine(
    settings.DB_DSN,
    echo=settings.DB_ECHO,
    future=True,
)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True, autoflush=False)


async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()


engine_demo = create_async_engine(
    settings.DB_DEMO_DSN,
    echo=settings.DB_DEMO_ECHO,
    future=True,
)
async_session_demo = async_sessionmaker(engine_demo, expire_on_commit=False, class_=AsyncSession, future=True, autoflush=False)


async def get_db_demo():
    db = async_session_demo()
    try:
        yield db
    finally:
        await db.close()
