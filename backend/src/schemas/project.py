from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.enums import Project


class Member(BaseModel):
    gitlab_user_id: int
    role: str


class ProjectDetail(BaseModel):
    name: str
    project_type: Project
    members: list[Member]


class ProjectCreated(BaseModel):
    repo_url: str
    project_id: UUID


class ProjectSummary(BaseModel):
    id: UUID
    name: str
    url_repository: str
    created_at: datetime
