import asyncio
from dataclasses import dataclass
from uuid import UUID

import logfire
from httpx import AsyncClient, Response

from src.builders import TemplateInterfaceBuilder
from src.database.models import Project
from src.enums import Environment
from src.errors import GitLabError, LogfireError, ProjectNotFoundError, SonarQubeError
from src.integrations.gitlab import AccessLevel, GitLabClient, GitLabMember, GitLabProject
from src.integrations.logfire import ERROR_ALERT_QUERY, LogfireChannel, LogfireClient, LogfireProject
from src.integrations.sonarqube import SonarQubeClient
from src.integrations.sonarqube.schemas import QualityGateStatus
from src.repositories import ProjectRepository
from src.schemas import (
    BuilderProjectData,
    Member,
    ProjectCreated,
    ProjectDetail,
    ProjectOverview,
    ProjectSummary,
    StageStatus,
)
from src.utils import slugify

ROLE_TO_ACCESS_LEVEL: dict[str, AccessLevel] = {
    "developer": AccessLevel.DEVELOPER,
    "maintainer": AccessLevel.MAINTAINER,
    "reporter": AccessLevel.REPORTER,
}

HEALTH_CHECK_TIMEOUT: int = 5


@dataclass
class ProjectService:
    gitlab: GitLabClient
    sonarqube: SonarQubeClient
    logfire: LogfireClient
    repository: ProjectRepository
    template_builder: TemplateInterfaceBuilder
    webhook_base_url: str
    sonarqube_alm_setting: str | None = None

    async def create_project(self, project: ProjectDetail, user_id: UUID) -> ProjectCreated:
        gitlab_project: GitLabProject = await self._setup_gitlab_project(project)
        sonarqube_created: bool = False
        project_key: str = slugify(project.name)

        try:
            await self._setup_sonarqube_project(
                project_name=project.name,
                gitlab_project_id=gitlab_project.id,
            )
            sonarqube_created = True

            logfire_project: LogfireProject = await self._setup_logfire_project(
                project_name=project.name,
                description=project.description or "",
            )

            db_project: Project = await self.repository.create(
                name=project.name,
                description=project.description,
                id_user=user_id,
                id_project_gitlab=gitlab_project.id,
                url_repository=gitlab_project.ssh_url_to_repo,
                id_project_logfire=str(logfire_project.id),
            )

            return ProjectCreated(repo_url=gitlab_project.ssh_url_to_repo, project_id=db_project.id)

        except (SonarQubeError, LogfireError) as e:
            logfire.error("Project creation failed, rolling back: {error}", error=str(e))
            await self._rollback_project_creation(
                gitlab_project_id=gitlab_project.id,
                project_key=project_key if sonarqube_created else None,
            )
            raise

    async def _rollback_project_creation(
        self,
        gitlab_project_id: int,
        project_key: str | None = None,
    ) -> None:
        try:
            await self.gitlab.delete_project(project_id=gitlab_project_id)
        except GitLabError:
            logfire.error("Failed to rollback GitLab project {id}", id=gitlab_project_id)

        if project_key:
            try:
                await self.sonarqube.delete_project(project_key=project_key)
            except SonarQubeError:
                logfire.error("Failed to rollback SonarQube project {key}", key=project_key)

    async def _setup_gitlab_project(self, project: ProjectDetail) -> GitLabProject:
        gitlab_project: GitLabProject = await self.gitlab.create_project(
            name=project.name,
            visibility="private",
            initialize_with_readme=False,
        )

        files: dict[str, str] = self.template_builder.build(
            data=BuilderProjectData(
                project_name=project.name,
                url_repository=gitlab_project.ssh_url_to_repo,
                codeowners=project.members,
            ),
        )

        await self.gitlab.initialize_repository(
            project_id=gitlab_project.id,
            files=files,
            commit_message="chore: Initial project setup [skip ci]",
        )

        await self.gitlab.create_branch(
            project_id=gitlab_project.id,
            branch_name="develop",
            from_branch="main",
        )

        await self._protect_branches(project_id=gitlab_project.id)

        await self._add_members(project_id=gitlab_project.id, members=project.members)

        return gitlab_project

    async def _setup_sonarqube_project(self, project_name: str, gitlab_project_id: int) -> None:
        project_key: str = slugify(project_name)

        await self.sonarqube.create_project(
            project_name=project_name,
            project_key=project_key,
        )

        await self.sonarqube.generate_project_token(
            project_key=project_key,
            token_name=f"{project_key}-token",
        )

        if self.sonarqube_alm_setting:
            await self.sonarqube.set_gitlab_binding(
                project_key=project_key,
                alm_setting=self.sonarqube_alm_setting,
                gitlab_project_id=gitlab_project_id,
            )

    async def _setup_logfire_project(self, project_name: str, description: str = "") -> LogfireProject:
        logfire_project: LogfireProject = await self.logfire.create_project(
            project_name=slugify(project_name),
            description=description,
        )
        await self.logfire.create_write_token(project_id=str(logfire_project.id))

        webhook_url: str = f"{self.webhook_base_url}webhooks/logfire/alerts"
        channel: LogfireChannel = await self.logfire.create_channel(
            label=f"{project_name}-alerts",
            webhook_url=webhook_url,
        )

        await self.logfire.create_alert(
            project_id=str(logfire_project.id),
            name=f"{project_name} error alert",
            description=f"Alert on error-level logs for {project_name}",
            query=ERROR_ALERT_QUERY,
            channel_ids=[str(channel.id)],
        )

        return logfire_project

    async def _check_environment_status(self, environment: Environment, domain: str) -> StageStatus:
        url: str = f"https://{environment.value}.{domain}"
        try:
            async with AsyncClient(timeout=HEALTH_CHECK_TIMEOUT) as client:
                response: Response = await client.get(url=url)
                return StageStatus(stage=environment, is_ready=response.status_code == 200)
        except Exception:
            return StageStatus(stage=environment, is_ready=False)

    async def _get_stages(self, domain: str | None) -> list[StageStatus]:
        if not domain:
            return []
        results: list[StageStatus] = await asyncio.gather(
            *[self._check_environment_status(environment=environment, domain=domain) for environment in Environment]
        )
        return list(results)

    async def get_project_overview(self, user_id: UUID, project_id: UUID) -> ProjectOverview:
        project: Project | None = await self.repository.get_by_id(project_id)

        if not project or project.id_user != user_id:
            raise ProjectNotFoundError()

        project_key: str = project.name.lower().replace(" ", "-")
        quality_gate: QualityGateStatus = await self.sonarqube.get_quality_gate_status(project_key=project_key)
        members: list[GitLabMember] = await self.gitlab.list_project_members(project_id=project.id_project_gitlab)
        stages: list[StageStatus] = await self._get_stages(domain=project.web_domain)

        return ProjectOverview(
            id=project.id,
            name=project.name,
            url_repository=project.url_repository,
            created_at=project.created_at,
            quality_gate=quality_gate,
            members=members,
            stages=stages,
        )

    async def list_projects(self, user_id: UUID) -> list[ProjectSummary]:
        projects: list[Project] = await self.repository.list_by_user(user_id)
        return [
            ProjectSummary(
                id=project.id,
                name=project.name,
                url_repository=project.url_repository,
                created_at=project.created_at,
            )
            for project in projects
        ]

    async def list_all_projects(self) -> list[ProjectSummary]:
        projects: list[Project] = await self.repository.list_all_repositories()
        return [
            ProjectSummary(
                id=project.id,
                name=project.name,
                url_repository=project.url_repository,
                created_at=project.created_at,
            )
            for project in projects
        ]

    async def _protect_branches(self, project_id: int) -> None:
        await self.gitlab.update_branch_protection(
            project_id=project_id,
            branch_name="main",
            push_access_level=AccessLevel.NO_ACCESS,
            merge_access_level=AccessLevel.MAINTAINER,
        )

        await self.gitlab.protect_branch(
            project_id=project_id,
            branch_name="develop",
            push_access_level=AccessLevel.NO_ACCESS,
            merge_access_level=AccessLevel.DEVELOPER,
        )

        for pattern in ("release/*", "hotfix/*"):
            await self.gitlab.protect_branch(
                project_id=project_id,
                branch_name=pattern,
                push_access_level=AccessLevel.NO_ACCESS,
                merge_access_level=AccessLevel.MAINTAINER,
            )

    async def _add_members(self, project_id: int, members: list[Member]) -> None:
        for member in members:
            access_level: AccessLevel = ROLE_TO_ACCESS_LEVEL.get(member.role.lower(), AccessLevel.DEVELOPER)
            await self.gitlab.add_member_to_project(
                project_id=project_id,
                user_name=member.gitlab_user_name,
                access_level=access_level,
            )
