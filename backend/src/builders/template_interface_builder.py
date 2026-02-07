from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel

from src.schemas import BuilderProjectData, Member
from src.utils.template_generator import TemplateGenerator


@dataclass
class TemplateInterfaceBuilder(ABC):
    template_generator: TemplateGenerator

    @abstractmethod
    def build(
        self,
        data: BuilderProjectData,
    ) -> dict[str, str]: ...

    @abstractmethod
    def build_root_files(self, data: BuilderProjectData) -> dict[str, str]: ...

    @abstractmethod
    def build_docker_files(self, data: BuilderProjectData) -> dict[str, str]: ...

    @abstractmethod
    def build_ci_files(self, data: BuilderProjectData) -> dict[str, str]: ...

    @abstractmethod
    def build_package_files(self, data: BuilderProjectData) -> dict[str, str]: ...

    @abstractmethod
    def build_source_files(self, data: BuilderProjectData) -> dict[str, str]: ...

    @abstractmethod
    def build_alembic_files(self) -> dict[str, str]: ...

    @abstractmethod
    def build_init_files(self) -> dict[str, str]: ...

    @abstractmethod
    def build_test_files(self) -> dict[str, str]: ...

    def _render(self, template_path: str, data: BaseModel | None = None) -> str:
        return self.template_generator.generate(
            template_path=Path(template_path),
            template_data=data,
        )

    def _generate_codeowners(self, members: list[Member]) -> str:
        maintainers: list[str] = [
            f"@{member.gitlab_user_name}" for member in members if member.role.lower() == "maintainer"
        ]
        developers: list[str] = [
            f"@{member.gitlab_user_name}" for member in members if member.role.lower() in ("developer", "maintainer")
        ]

        lines: list[str] = []

        if maintainers:
            lines.append(f"* {' '.join(maintainers)}")

        if developers:
            lines.append(f"src/ {' '.join(developers)}")
            lines.append(f"tests/ {' '.join(developers)}")

        return "\n".join(lines) + "\n"
