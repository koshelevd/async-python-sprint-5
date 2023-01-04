from pydantic import PostgresDsn

from settings.base import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int

    def get_db_url(self, alembic: bool = False):
        return PostgresDsn.build(
            scheme="postgresql" if alembic else "postgresql+asyncpg",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            path=f"/{self.DB_NAME}",
            port=str(self.DB_PORT),
        )


db_settings = Settings()
