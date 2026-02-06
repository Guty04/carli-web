from .auth import AuthenticationError, AuthorizationError
from .gitlab import (
    GitLabAPIError,
    GitLabAuthenticationError,
    GitLabError,
    GitLabNotFoundError,
)

__all__: list[str] = [
    "AuthenticationError",
    "AuthorizationError",
    "GitLabAPIError",
    "GitLabAuthenticationError",
    "GitLabError",
    "GitLabNotFoundError",
]
