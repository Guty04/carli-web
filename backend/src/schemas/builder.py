from pydantic import BaseModel

from .project import Member


class BuilderProjectData(BaseModel):
    project_name: str
    url_repository: str
    codeowners: list[Member]
