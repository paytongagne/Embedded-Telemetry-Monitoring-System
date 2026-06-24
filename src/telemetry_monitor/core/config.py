from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Embedded Telemetry Monitoring System"
    app_version: str = "0.3.0"
    environment: str = Field(default="local", validation_alias="APP_ENV")
    database_path: Path = Field(default=Path("data/telemetry.db"), validation_alias="DATABASE_PATH")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    enable_sqlite_wal: bool = Field(default=True, validation_alias="ENABLE_SQLITE_WAL")


@lru_cache
def get_settings() -> Settings:
    return Settings()
