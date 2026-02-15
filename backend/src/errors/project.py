class ProjectError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ProjectNotFoundError(ProjectError):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class ProjectAlreadyExistsError(ProjectError):
    def __init__(self, message: str = "A project with this name already exists") -> None:
        super().__init__(message)
