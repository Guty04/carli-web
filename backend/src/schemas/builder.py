from pydantic import BaseModel

from .project import Member


class BuilderProjectData(BaseModel):
    project_name: str
    github_url: str
    codeowners: list[Member]
