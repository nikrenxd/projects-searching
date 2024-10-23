from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")


class Config(BaseConfig):
    DB_URL: PostgresDsn
    REDIS_URL: RedisDsn

    BASE_URL: str


settings = Config()
