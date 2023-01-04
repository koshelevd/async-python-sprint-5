from settings.base import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    SERVER_HOST: str
    SERVER_PORT: int
    PROJECT_NAME: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str


api_settings = Settings()
