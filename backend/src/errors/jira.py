class JiraError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class JiraAPIError(JiraError):
    def __init__(self, message: str = "Jira API error") -> None:
        super().__init__(message)


class JiraAuthenticationError(JiraError):
    def __init__(self, message: str = "Invalid or expired Jira credentials") -> None:
        super().__init__(message)
