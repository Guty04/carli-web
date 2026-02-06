class GitLabError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class GitLabAPIError(GitLabError):
    def __init__(self, message: str = "GitLab API error") -> None:
        super().__init__(message)


class GitLabAuthenticationError(GitLabError):
    def __init__(self, message: str = "Invalid or expired GitLab token") -> None:
        super().__init__(message)


class GitLabNotFoundError(GitLabError):
    def __init__(self, message: str = "Resource not found: projects") -> None:
        super().__init__(message)
