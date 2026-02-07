from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.enums import Environment, Project
from src.integrations.gitlab.schemas import GitLabMember
from src.integrations.sonarqube.schemas import QualityGateStatus


class Member(BaseModel):
    gitlab_user_name: str
    role: str


class ProjectDetail(BaseModel):
    name: str
    description: str | None = None
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


class StageStatus(BaseModel):
    stage: Environment
    is_ready: bool


class ProjectOverview(ProjectSummary):
    quality_gate: QualityGateStatus
    members: list[GitLabMember]
    stages: list[StageStatus]
