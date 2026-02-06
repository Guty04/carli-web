from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from cli.utils import TemplateRender  # type:ignore


@dataclass
class BaseProject(ABC):
    templates_path: Path = Path(__file__).parent.parent / "templates"
    renderer = TemplateRender(templates_directory=templates_path)  # type:ignore

    @abstractmethod
    def inicialice_project(
        self,
        project_name: str,
        git: bool,
        install_packages: bool,
    ) -> None: ...

    @abstractmethod
    def get_agent_file(self) -> Path: ...

    @abstractmethod
    def get_debug_file(self) -> Path: ...

    @abstractmethod
    def get_dockerfile(self) -> Path: ...

    @abstractmethod
    def get_env_file(self) -> Path: ...

    @abstractmethod
    def get_example_env_file(self) -> Path: ...

    @abstractmethod
    def get_gitignore_file(self) -> Path: ...

    @abstractmethod
    def get_init_file(self) -> str: ...

    @abstractmethod
    def get_precommit_file(self) -> Path: ...

    @abstractmethod
    def get_readme_file(self) -> Path: ...

    @abstractmethod
    def set_debug_file(self, project_directory: Path) -> None: ...

    @abstractmethod
    def set_general_files(self, project_directory: Path) -> None: ...

    @abstractmethod
    def set_packages_files(self, project_directory: Path) -> None: ...

    @abstractmethod
    def create_source_directories(self, project_directory: Path) -> None: ...

    @abstractmethod
    def create_tests_directories(self, project_directory: Path) -> None: ...

    def _create_directory(self, project_directory: Path, directory: str) -> None:
        directory_to_create: Path = project_directory / directory

        directory_to_create.mkdir()

    def _create_base_directories(self, project_directory: Path) -> None:
        project_directory.mkdir()

        for directory in ["src", "tests", ".vscode"]:
            self._create_directory(
                project_directory=project_directory, directory=directory
            )
