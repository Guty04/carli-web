from dataclasses import dataclass

from src.schemas import BuilderProjectData

from .template_interface_builder import TemplateInterfaceBuilder


@dataclass
class BackendBuilder(TemplateInterfaceBuilder):
    def build(
        self,
        data: BuilderProjectData,
    ) -> dict[str, str]:
        return self._build_backend(data)

    def _build_backend(self, data: BuilderProjectData) -> dict[str, str]:
        files: dict[str, str] = {}

        files.update(self.build_root_files(data))
        files.update(self.build_docker_files(data))
        files.update(self.build_ci_files(data))
        files.update(self.build_package_files(data))
        files.update(self.build_source_files(data))
        files.update(self.build_init_files())
        files.update(self.build_test_files())

        return files

    def build_root_files(self, data: BuilderProjectData) -> dict[str, str]:
        files: dict[str, str] = {}

        root_templates: dict[str, str] = {
            "README.md": "readme/backend.README.md.j2",
            ".gitignore": "git/backend.gitignore.j2",
            "AGENT.md": "agent/backend.AGENT.md.j2",
            ".pre-commit-config.yaml": "pre-commit/backend.pre-commit.yaml.j2",
            ".vscode/launch.json": "debug/backend.launch.json.j2",
            "example.env": "env/backend.example.env.j2",
            "alembic.ini": "alembic/backend.alembic.ini.j2",  # TODO: Agregar los archivos de alembic
        }

        for file_path, template in root_templates.items():
            files[file_path] = self._render(template_path=template, data=data)

        if data.codeowners:
            files["CODEOWNERS"] = self._generate_codeowners(owners=data.codeowners)

        return files

    def build_docker_files(self, data: BuilderProjectData) -> dict[str, str]:
        files: dict[str, str] = {}

        docker_templates: dict[str, str] = {
            "Dockerfile": "docker/backend.Dockerfile.j2",
            "docker-compose.yml": "docker/backend.docker-compose.j2",
        }

        for file_path, template in docker_templates.items():
            files[file_path] = self._render(template_path=template, data=data)

        return files

    def build_ci_files(self, data: BuilderProjectData) -> dict[str, str]:
        return {".gitlab-ci.yml": self._render("ci/backend.gitlab-ci.yml.j2", data)}

    def build_package_files(self, data: BuilderProjectData) -> dict[str, str]:
        return {"pyproject.toml": self._render("packages/backend.package.j2", data)}

    def build_source_files(self, data: BuilderProjectData) -> dict[str, str]:
        files: dict[str, str] = {}

        source_templates: dict[str, str] = {
            "src/main.py": "main/backend.main.py.j2",
            "src/configurations/config.py": "configurations/backend.config.py.j2",
            "src/enums/environment.py": "enums/backend.environment.py.j2",
        }

        for file_path, template in source_templates.items():
            files[file_path] = self._render(template_path=template, data=data)

        return files

    def build_init_files(self) -> dict[str, str]:
        directories: list[str] = [
            "src",
            "src/configurations",
            "src/database",
            "src/database/models",
            "src/enums",
            "src/errors",
            "src/repositories",
            "src/routes",
            "src/routes/dependencies",
            "src/schemas",
            "src/services",
        ]
        return {f"{directory}/__init__.py": "" for directory in directories}

    def build_test_files(self) -> dict[str, str]:
        test_directories: list[str] = [
            "tests",
            "tests/e2e",
            "tests/integration",
            "tests/unit",
        ]
        return {f"{directory}/__init__.py": "" for directory in test_directories}
