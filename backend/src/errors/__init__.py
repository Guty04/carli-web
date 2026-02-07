from .auth import AuthenticationError, AuthorizationError
from .gemini import GeminiAPIError, GeminiError
from .gitlab import (
    GitLabAPIError,
    GitLabAuthenticationError,
    GitLabError,
    GitLabNotFoundError,
)
from .jira import JiraAPIError, JiraAuthenticationError, JiraError
from .logfire import (
    LogfireAPIError,
    LogfireAuthenticationError,
    LogfireError,
)
from .project import ProjectNotFoundError
from .sonarqube import (
    SonarQubeAPIError,
    SonarQubeAuthenticationError,
    SonarQubeError,
    SonarQubeNotFoundError,
)

__all__: list[str] = [
    "AuthenticationError",
    "AuthorizationError",
    "GeminiAPIError",
    "GeminiError",
    "GitLabAPIError",
    "GitLabAuthenticationError",
    "GitLabError",
    "GitLabNotFoundError",
    "JiraAPIError",
    "JiraAuthenticationError",
    "JiraError",
    "LogfireAPIError",
    "LogfireAuthenticationError",
    "LogfireError",
    "SonarQubeAPIError",
    "SonarQubeAuthenticationError",
    "SonarQubeError",
    "SonarQubeNotFoundError",
    "ProjectNotFoundError",
]
