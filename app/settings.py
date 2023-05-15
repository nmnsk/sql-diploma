from pydantic import BaseSettings
from sqlalchemy.engine.url import URL


class Settings(BaseSettings):
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "qwerty"
    DB_DATABASE: str = "service"
    DB_ECHO: bool = False

    @property
    def DB_DSN(self) -> URL:
        return URL.create(self.DB_DRIVER, self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_DATABASE)

    DB_DEMO_DRIVER: str = "postgresql+asyncpg"
    DB_DEMO_HOST: str = "db_demo"
    DB_DEMO_PORT: int = 5433
    DB_DEMO_USER: str = "postgres"
    DB_DEMO_PASSWORD: str = "qwerty"
    DB_DEMO_DATABASE: str = "demo"
    DB_DEMO_ECHO: bool = False

    @property
    def DB_DEMO_DSN(self) -> URL:
        return URL.create(self.DB_DRIVER, self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_DATABASE)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
