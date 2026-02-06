from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template
from pydantic import BaseModel


@dataclass
class TemplateGenerator:
    templates_directory: Path

    def __post_init__(self) -> None:
        self.environment = Environment(
            loader=FileSystemLoader(self.templates_directory),
            autoescape=False,  # nosec
            keep_trailing_newline=True,
        )

    def generate(
        self,
        template_path: Path,
        template_data: BaseModel | None = None,
    ) -> str:
        template: Template = self.environment.get_template(template_path.as_posix())

        rendered_content: str = template.render(
            template_data.model_dump() if template_data else {}
        )

        return rendered_content

    def template_exists(self, template_path: Path) -> bool:
        full_path: Path = self.templates_directory / template_path
        return full_path.exists()
