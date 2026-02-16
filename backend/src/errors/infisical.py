class InfisicalError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InfisicalAPIError(InfisicalError):
    def __init__(self, message: str = "Infisical API error") -> None:
        super().__init__(message)


class InfisicalAuthenticationError(InfisicalError):
    def __init__(self, message: str = "Invalid or expired Infisical token") -> None:
        super().__init__(message)
