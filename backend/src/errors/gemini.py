class GeminiError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class GeminiAPIError(GeminiError):
    def __init__(self, message: str = "Gemini API error") -> None:
        super().__init__(message)
