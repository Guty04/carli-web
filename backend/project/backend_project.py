from dataclasses import dataclass, field
from pathlib import Path

from cli.tools import init_alembic, init_git_repo, install_dependencies  # type:ignore
from cli.tools.uv import create_venv  # type:ignore
from pydantic import BaseModel, HttpUrl

from .base_project import BaseProject


class BaseTemplate(BaseModel):
    project_name: str


class ReadmeTemplate(BaseTemplate):
    github_url: HttpUrl


@dataclass
class BackendProject(BaseProject):
    DIRECTORIES: list[Path] = field(
        default_factory=lambda: [
            Path("configurations"),
            Path("database"),
            Path("database/models"),
            Path("enums"),
            Path("errors"),
            Path("repositories"),
            Path("routes"),
            Path("routes/dependencies"),
            Path("schemas"),
            Path("services"),
        ]
    )

    def inicialice_project(
        self, project_name: str, git: bool, install_packages: bool
    ) -> None:
        project_directory: Path = Path.cwd() / project_name

        if project_directory.exists():
            raise ValueError(f"Project '{project_name}' already exists")

        self._create_base_directories(project_directory=project_directory)

        self.create_source_directories(project_directory=project_directory)

        self.create_tests_directories(project_directory=project_directory)

        self.set_debug_file(project_directory=project_directory)

        self.set_general_files(project_directory=project_directory)

        self.create_main_file(project_directory=project_directory)

        if git:
            init_git_repo(project_directory=str(project_directory))

        create_venv(project_path=project_directory)

        self.set_packages_files(project_directory=project_directory)

        if install_packages:
            install_dependencies(project_path=project_directory)
            init_alembic(project_path=project_directory)

        source_code: Path = project_directory / "src"

        settings_template = Path("configurations/backend.config.py.j2")
        if self.renderer.template_exists(template_path=settings_template):  # type:ignore
            self.renderer.render_template(  # type:ignore
                template_path=settings_template,
                destination_path=source_code / "configurations" / "config.py",
                template_data=BaseTemplate(project_name=project_name),
            )

        environment_template = Path("enums/backend.environment.py.j2")
        if self.renderer.template_exists(environment_template):  # type:ignore
            self.renderer.render_template(  # type:ignore
                template_path=environment_template,
                destination_path=source_code / "enums" / "environment.py",
            )

    def get_agent_file(self) -> Path:
        return Path("agent/backend.AGENT.md.j2")

    def get_debug_file(self) -> Path:
        return Path("debug/backend.launch.json.j2")

    def get_dockerfile(self) -> Path:
        return Path("docker/backend.Dockerfile.j2")

    def get_docker_compose_file(self) -> Path:
        return Path("docker/backend.docker-compose.j2")

    def get_env_file(self) -> Path:
        return Path("env/backend.env.j2")

    def get_example_env_file(self) -> Path:
        return Path("env/backend.example.env.j2")

    def get_gitignore_file(self) -> Path:
        return Path("git/backend.gitignore.j2")

    def get_init_file(self) -> str:
        return "__init__.py"

    def get_main_file(self) -> Path:
        return Path("main/backend.main.py.j2")

    def get_precommit_file(self) -> Path:
        return Path("pre-commit/backend.pre-commit.yaml.j2")

    def get_pyproject_file(self) -> Path:
        return Path("packages/backend.package.j2")

    def get_readme_file(self) -> Path:
        return Path("readme/backend.README.md.j2")

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
        pyproject_template: Path = self.get_pyproject_file()

        if self.renderer.template_exists(pyproject_template):  # type:ignore
            self.renderer.render_template(  # type:ignore
                template_path=pyproject_template,
                destination_path=project_directory / "pyproject.toml",
                template_data=BaseTemplate(project_name=project_directory.name),
            )

    def create_main_file(self, project_directory: Path) -> None:
        source_code: Path = project_directory / "src"
        main_template: Path = self.get_main_file()

        if self.renderer.template_exists(template_path=main_template):  # type:ignore
            self.renderer.render_template(  # type:ignore
                template_path=main_template,
                destination_path=source_code / "main.py",
                template_data=BaseTemplate(project_name=project_directory.name),
            )

    def create_source_directories(self, project_directory: Path) -> None:
        source_code: Path = project_directory / "src"

        for directory in self.DIRECTORIES:
            layer_directory: Path = source_code / directory
            layer_directory.mkdir(parents=True)
            init_file: str = self.get_init_file()

            if init_file:
                (layer_directory / init_file).touch()

    def create_tests_directories(self, project_directory: Path) -> None:
        test: Path = project_directory / "tests"

        for test_directory in ["e2e", "integration", "unit"]:
            test_subdirectory: Path = test / test_directory
            test_subdirectory.mkdir()
