
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_username: str
    postgres_password: str
    db_ref: str
    postgres_host: str = "localhost"
    postgres_port: int = 5444

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_username}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.db_ref}"
        )

@lru_cache
def get_settings() -> Settings:
    return Settings()
