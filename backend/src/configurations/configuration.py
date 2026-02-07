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
    APP_NAME: str
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    CORS_ORIGIN: list[str] = ["http://localhost:3000"]
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES: int = 30
    LOGFIRE_TOKEN: str
    LOGFIRE_API_URL: HttpUrl
    GITLAB_API_URL: HttpUrl
    GITLAB_PRIVATE_TOKEN: str
    GITLAB_NAMESPACE_ID: int
    SONARQUBE_API_URL: HttpUrl
    SONARQUBE_TOKEN: str
    SONARQUBE_ALM_SETTING: str | None = None
    JIRA_API_URL: HttpUrl
    JIRA_TOKEN: str
    JIRA_USER_EMAIL: str
    JIRA_PROJECT_KEY: str
    GEMINI_API_KEY: str
    GEMINI_MODEL: str
    WEBHOOK_BASE_URL: HttpUrl


configuration = Configuration()  # type:ignore
