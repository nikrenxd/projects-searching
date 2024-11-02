from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")


class Config(BaseConfig):
    DB_URL: str
    REDIS_URL: str

    BASE_URL: str


settings = Config()
