from pydantic import HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.enums.environment import Environment


class Configuration(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    APP_NAME: str = "backend"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    CORS_ORIGIN: list[str] = ["http://localhost:3000"]
    DATABASE_URL: PostgresDsn = PostgresDsn(
        f"postgresql+asyncpg://user:password@localhost:5432/{APP_NAME}"
    )
    SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES: int = 30
    LOGFIRE_TOKEN: str | None = None
    LOGFIRE_API_URL: HttpUrl
    GITLAB_API_URL: HttpUrl
    GITLAB_PRIVATE_TOKEN: str = ""
    GITLAB_NAMESPACE_ID: int = 0
    SONARQUBE_API_URL: HttpUrl
    SONARQUBE_TOKEN: str = ""
    JIRA_API_URL: HttpUrl


configuration = Configuration()  # type:ignore
