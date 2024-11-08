from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")


class Config(BaseConfig):
    MODE: Literal["TEST", "DEV"]
    DB_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/postgres"
    )
    TEST_DB_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/test_postgres"
    )
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    BASE_URL: str = Field(default="http:///")


settings = Config()
