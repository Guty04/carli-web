from .backend_project import BackendProject
from .base_project import BaseProject
from .frontend_project import FrontendNextProject, FrontendQuasarProject

__all__: list[str] = [
    "BaseProject",
    "BackendProject",
    "FrontendNextProject",
    "FrontendQuasarProject",
]
