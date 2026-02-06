class SonarQubeError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class SonarQubeAPIError(SonarQubeError):
    def __init__(self, message: str = "SonarQube API error") -> None:
        super().__init__(message)


class SonarQubeAuthenticationError(SonarQubeError):
    def __init__(self, message: str = "Invalid or expired SonarQube token") -> None:
        super().__init__(message)


class SonarQubeNotFoundError(SonarQubeError):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message)
