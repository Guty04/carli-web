from dataclasses import dataclass, field
from pathlib import Path

from cli.tools import init_git_repo  # type:ignore
from cli.tools.npm import (  # type:ignore
    add_dependencies,  # type:ignore
    create_next_app,  # type:ignore
    create_quasar_app,  # type:ignore
)
from pydantic import BaseModel, HttpUrl

from .base_project import BaseProject


class BaseTemplate(BaseModel):
    project_name: str


class ReadmeTemplate(BaseTemplate):
    github_url: HttpUrl


@dataclass
class FrontendNextProject(BaseProject):
    DIRECTORIES: list[Path] = field(
        default_factory=lambda: [
            Path("app"),
            Path("components"),
            Path("hooks"),
            Path("lib"),
            Path("schemas"),
            Path("services"),
            Path("stories"),
            Path("styles"),
            Path("types"),
        ]
    )

    def inicialice_project(
        self, project_name: str, git: bool, install_packages: bool
    ) -> None:
        project_directory: Path = Path.cwd() / project_name

        if project_directory.exists():
            raise ValueError(f"Project '{project_name}' already exists")

        # 1. Create Base App using CLI
        create_next_app(project_name=project_name, cwd=Path.cwd())

        # 2. Add Dependencies (Zod, React Query)
        add_dependencies(
            project_path=project_directory,
            dependencies=["zod", "@tanstack/react-query"],
        )

        # 3. Add Dev Dependencies (Storybook, Husky)
        add_dependencies(
            project_path=project_directory,
            dependencies=["storybook", "husky"],
            dev=True,
        )

        # 4. Create Source Directories
        self.create_source_directories(project_directory=project_directory)

        # 5. Create Tests
        self.create_tests_directories(project_directory=project_directory)

        # 6. Set Config Files
        self.set_debug_file(project_directory=project_directory)
        self.set_general_files(project_directory=project_directory)

        if git:
            init_git_repo(project_directory=str(project_directory))

    def get_agent_file(self) -> Path:
        return Path("agent/frontend_next.AGENT.md.j2")

    def get_debug_file(self) -> Path:
        return Path("debug/frontend_next.launch.json.j2")

    def get_dockerfile(self) -> Path:
        return Path("docker/frontend_next.Dockerfile.j2")

    def get_env_file(self) -> Path:
        return Path("env/frontend_next.env.j2")

    def get_example_env_file(self) -> Path:
        return Path("env/frontend_next.example.env.j2")

    def get_gitignore_file(self) -> Path:
        return Path("git/frontend_next.gitignore.j2")

    def get_init_file(self) -> str:
        return "index.ts"

    def get_precommit_file(self) -> Path:
        return Path("pre-commit/frontend_next.pre-commit.yaml.j2")

    def get_pyproject_file(self) -> Path:
        return Path("packages/frontend_next.package.json.j2")

    def get_readme_file(self) -> Path:
        return Path("readme/frontend_next.README.md.j2")

    def set_debug_file(self, project_directory: Path) -> None:
        debug_file_destination_path: Path = (
            project_directory / ".vscode" / "launch.json"
        )

        debug_template: Path = self.get_debug_file()

        if not debug_file_destination_path.parent.exists():
            debug_file_destination_path.parent.mkdir(exist_ok=True, parents=True)

        if self.renderer.template_exists(template_path=debug_template):  # type:ignore
            self.renderer.render_template(  # type:ignore
                template_path=debug_template,
                destination_path=debug_file_destination_path,
                template_data=BaseTemplate(project_name=project_directory.name),
            )

    def set_general_files(self, project_directory: Path) -> None:
        self.renderer.render_template(  # type:ignore
            template_path=self.get_agent_file(),
            destination_path=project_directory / "AGENT.md",
        )

        self.renderer.render_template(  # type:ignore
            template_path=self.get_dockerfile(),
            destination_path=project_directory / "Dockerfile",
        )

        self.renderer.render_template(  # type:ignore
            template_path=self.get_readme_file(),
            destination_path=project_directory / "README.md",
            template_data=ReadmeTemplate(
                project_name=project_directory.name,
                github_url=HttpUrl("http://localhost"),
            ),
        )

        self.renderer.render_template(  # type:ignore
            template_path=self.get_env_file(),
            destination_path=project_directory / ".env",
            template_data=BaseTemplate(project_name=project_directory.name),
        )

        self.renderer.render_template(  # type:ignore
            template_path=self.get_example_env_file(),
            destination_path=project_directory / "example.env",
            template_data=BaseTemplate(project_name=project_directory.name),
        )

        self.renderer.render_template(  # type:ignore
            template_path=self.get_gitignore_file(),
            destination_path=project_directory / ".gitignore",
        )

        self.renderer.render_template(  # type:ignore
            template_path=self.get_precommit_file(),
            destination_path=project_directory / ".pre-commit-config.yaml",
        )

    def set_packages_files(self, project_directory: Path) -> None:
        package_template: Path = self.get_pyproject_file()

        if self.renderer.template_exists(package_template):  # type:ignore
            self.renderer.render_template(  # type:ignore
                template_path=package_template,
                destination_path=project_directory / "package.json",
                template_data=BaseTemplate(project_name=project_directory.name),
            )

    def create_source_directories(self, project_directory: Path) -> None:
        source_code: Path = project_directory / "src"

        for directory in self.DIRECTORIES:
            layer_directory: Path = source_code / directory
            layer_directory.mkdir(parents=True, exist_ok=True)

    def create_tests_directories(self, project_directory: Path) -> None:
        test: Path = project_directory / "tests"
        for test_directory in ["e2e", "unit"]:
            test_subdirectory: Path = test / test_directory
            test_subdirectory.mkdir(parents=True, exist_ok=True)


@dataclass
class FrontendQuasarProject(BaseProject):
    DIRECTORIES: list[Path] = field(
        default_factory=lambda: [
            Path("boot"),
            Path("components"),
            Path("css"),
            Path("layouts"),
            Path("pages"),
            Path("router"),
            Path("stores"),
        ]
    )

    def inicialice_project(
        self, project_name: str, git: bool, install_packages: bool
    ) -> None:
        project_directory: Path = Path.cwd() / project_name

        if project_directory.exists():
            raise ValueError(f"Project '{project_name}' already exists")

        # 1. Create Quasar App
        create_quasar_app(project_name=project_name, cwd=Path.cwd())

        # 2. Add Dependencies
        add_dependencies(
            project_path=project_directory,
            dependencies=["pinia"],
        )
        add_dependencies(
            project_path=project_directory,
            dependencies=["husky"],
            dev=True,
        )

        # 3. Create Source Directories
        self.create_source_directories(project_directory=project_directory)

        # 4. Create Tests
        self.create_tests_directories(project_directory=project_directory)

        # 5. Set Config Files
        self.set_debug_file(project_directory=project_directory)
        self.set_general_files(project_directory=project_directory)

        if git:
            init_git_repo(project_directory=str(project_directory))

    def get_agent_file(self) -> Path:
        return Path("agent/frontend_quasar.AGENT.md.j2")

    def get_debug_file(self) -> Path:
        return Path("debug/frontend_quasar.launch.json.j2")

    def get_dockerfile(self) -> Path:
        return Path("docker/frontend_quasar.Dockerfile.j2")

    def get_env_file(self) -> Path:
        return Path("env/frontend_quasar.env.j2")

    def get_example_env_file(self) -> Path:
        return Path("env/frontend_quasar.example.env.j2")

    def get_gitignore_file(self) -> Path:
        return Path("git/frontend_quasar.gitignore.j2")

    def get_init_file(self) -> str:
        return ""

    def get_precommit_file(self) -> Path:
        return Path("pre-commit/frontend_quasar.pre-commit.yaml.j2")

    def get_pyproject_file(self) -> Path:
        return Path("packages/frontend_quasar.package.json.j2")

    def get_readme_file(self) -> Path:
        return Path("readme/frontend_quasar.README.md.j2")

    def set_debug_file(self, project_directory: Path) -> None:
        debug_file_destination_path: Path = (
            project_directory / ".vscode" / "launch.json"
        )
        debug_template: Path = self.get_debug_file()
        if self.renderer.template_exists(template_path=debug_template):  # type:ignore
            self.renderer.render_template(  # type:ignore
                template_path=debug_template,
                destination_path=debug_file_destination_path,
                template_data=BaseTemplate(project_name=project_directory.name),
            )

    def set_general_files(self, project_directory: Path) -> None:
        self.renderer.render_template(  # type:ignore
            template_path=self.get_agent_file(),
            destination_path=project_directory / "AGENT.md",
        )
        self.renderer.render_template(  # type:ignore
            template_path=self.get_dockerfile(),
            destination_path=project_directory / "Dockerfile",
        )
        self.renderer.render_template(  # type:ignore
            template_path=self.get_readme_file(),
            destination_path=project_directory / "README.md",
            template_data=ReadmeTemplate(
                project_name=project_directory.name,
                github_url=HttpUrl("http://localhost"),
            ),
        )
        self.renderer.render_template(  # type:ignore
            template_path=self.get_env_file(),
            destination_path=project_directory / ".env",
            template_data=BaseTemplate(project_name=project_directory.name),
        )
        self.renderer.render_template(  # type:ignore
            template_path=self.get_example_env_file(),
            destination_path=project_directory / "example.env",
            template_data=BaseTemplate(project_name=project_directory.name),
        )
        self.renderer.render_template(  # type:ignore
            template_path=self.get_gitignore_file(),
            destination_path=project_directory / ".gitignore",
        )
        self.renderer.render_template(  # type:ignore
            template_path=self.get_precommit_file(),
            destination_path=project_directory / ".pre-commit-config.yaml",
        )

    def set_packages_files(self, project_directory: Path) -> None:
        package_template: Path = self.get_pyproject_file()
        if self.renderer.template_exists(package_template):  # type:ignore
            self.renderer.render_template(  # type:ignore
                template_path=package_template,
                destination_path=project_directory / "package.json",
                template_data=BaseTemplate(project_name=project_directory.name),
            )

    def create_source_directories(self, project_directory: Path) -> None:
        source_code: Path = project_directory / "src"
        for directory in self.DIRECTORIES:
            layer_directory: Path = source_code / directory
            layer_directory.mkdir(parents=True, exist_ok=True)

    def create_tests_directories(self, project_directory: Path) -> None:
        test: Path = project_directory / "tests"
        for test_directory in ["e2e", "unit"]:
            test_subdirectory: Path = test / test_directory
            test_subdirectory.mkdir(exist_ok=True, parents=True)
