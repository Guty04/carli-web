from .auth import AuthenticationError, AuthorizationError
from .gitlab import (
    GitLabAPIError,
    GitLabAuthenticationError,
    GitLabError,
    GitLabNotFoundError,
)
from .logfire import (
    LogfireAPIError,
    LogfireAuthenticationError,
    LogfireError,
)
from .sonarqube import (
    SonarQubeAPIError,
    SonarQubeAuthenticationError,
    SonarQubeError,
    SonarQubeNotFoundError,
)

__all__: list[str] = [
    "AuthenticationError",
    "AuthorizationError",
    "GitLabAPIError",
    "GitLabAuthenticationError",
    "GitLabError",
    "GitLabNotFoundError",
    "LogfireAPIError",
    "LogfireAuthenticationError",
    "LogfireError",
    "SonarQubeAPIError",
    "SonarQubeAuthenticationError",
    "SonarQubeError",
    "SonarQubeNotFoundError",
]
