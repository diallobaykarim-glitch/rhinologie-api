from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "API Rhinologie"
    app_version: str = "1.0.0"
    environment: str = "local"
    database_url: str = "postgresql+psycopg://rhinologie:rhinologie@localhost:5432/rhinologie"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
