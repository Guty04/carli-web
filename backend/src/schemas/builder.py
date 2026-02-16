from pydantic import BaseModel

from .project import Member


class BuilderProjectData(BaseModel):
    project_name: str
    project_key: str
    description: str
    url_repository: str
    codeowners: list[Member]
    logfire_url: str | None = None
