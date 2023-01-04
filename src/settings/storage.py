from settings.base import BaseSettings


class Settings(BaseSettings):
    ROOT_DIR: str = "/storage"


storage_settings = Settings()
