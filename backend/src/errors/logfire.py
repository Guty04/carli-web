class LogfireError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class LogfireAPIError(LogfireError):
    def __init__(self, message: str = "Logfire CLI error") -> None:
        super().__init__(message)


class LogfireAuthenticationError(LogfireError):
    def __init__(self, message: str = "Invalid or expired Logfire token") -> None:
        super().__init__(message)
