from .auth import AuthenticationError, AuthorizationError
from .gitlab import (
    GitLabAPIError,
    GitLabAuthenticationError,
    GitLabError,
    GitLabNotFoundError,
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
    "SonarQubeAPIError",
    "SonarQubeAuthenticationError",
    "SonarQubeError",
    "SonarQubeNotFoundError",
]
