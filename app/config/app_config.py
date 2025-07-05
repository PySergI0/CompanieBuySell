__all__ = ["config"]

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class DatabaseConfig(BaseConfig):
    user: str
    password: str
    host: str
    name: str
    port: str

    class Config:
        env_prefix = "DB_"


class Config(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.db.user}:{self.db.password}@{self.db.host}:{self.db.port}/{self.db.name}"
        )

    @classmethod
    def load(cls) -> "Config":
        return cls()


config = Config.load()
