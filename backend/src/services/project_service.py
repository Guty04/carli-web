import asyncio
import secrets
from dataclasses import dataclass
from uuid import UUID

import logfire
from httpx import AsyncClient, Response

from src.builders import TemplateInterfaceBuilder
from src.database.models import Integration, Project
from src.enums import Environment
from src.enums import Integration as IntegrationEnum
from src.errors import (
    GitLabError,
    InfisicalError,
    JiraError,
    LogfireError,
    ProjectAlreadyExistsError,
    ProjectNotFoundError,
    SonarQubeError,
)
from src.integrations.gitlab import AccessLevel, GitLabClient, GitLabMember, GitLabProject
from src.integrations.infisical import InfisicalClient, InfisicalProject
from src.integrations.jira import JiraClient, JiraProject
from src.integrations.logfire import ERROR_ALERT_QUERY, LogfireChannel, LogfireClient, LogfireProject, LogfireWriteToken
from src.integrations.sonarqube import QualityGateStatus, SonarQubeClient, SonarQubeToken
from src.repositories import IntegrationRepository, ProjectRepository
from src.schemas import (
    BuilderProjectData,
    Member,
    ProjectCreated,
    ProjectDetail,
    ProjectOverview,
    ProjectSummary,
    StageStatus,
)
from src.utils import logfire_slug, slugify

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
    jira: JiraClient
    infisical: InfisicalClient
    repository: ProjectRepository
    integration_repository: IntegrationRepository
    template_builder: TemplateInterfaceBuilder
    webhook_base_url: str

    async def create_project(self, project: ProjectDetail, user_id: UUID) -> ProjectCreated:
        existing: Project | None = await self.repository.get_by_name(project.name)

        if existing:
            raise ProjectAlreadyExistsError()

        project_key: str = slugify(project.name)
        gitlab_project: GitLabProject = await self._setup_gitlab_project(project=project, project_key=project_key)
        infisical_project: InfisicalProject | None = None
        sonarqube_created: bool = False
        logfire_project: LogfireProject | None = None
        jira_project: JiraProject | None = None

        try:
            logfire_project = await self._setup_logfire_project(
                project_name=project.name,
                description=project.description,
            )

            infisical_project = await self._setup_infisical_project(
                project_name=project.name,
                project_description=project.description,
            )

            await self._setup_envs(
                infisical_project_id=infisical_project.id,
                logfire_project_id=logfire_project.id,
            )

            sonarqube_token: SonarQubeToken = await self._setup_sonarqube_project(
                project_key=project_key,
                project_name=project.name,
                gitlab_project_id=gitlab_project.id,
            )
            sonarqube_created = True

            await self.gitlab.create_ci_variable(
                project_id=gitlab_project.id,
                key="SONAR_TOKEN",
                value=sonarqube_token.token,
            )

            jira_project = await self._setup_jira_project(
                project_key=project_key,
                project_name=project.name,
                project_description=project.description,
            )

            db_project: Project = await self.repository.create(
                name=project.name,
                description=project.description,
                id_user=user_id,
                url_repository=gitlab_project.ssh_url_to_repo,
            )

            db_project.integrations.update(
                [
                    Integration(
                        project_id=db_project.id,
                        name=IntegrationEnum.GITLAB,
                        external_id=str(gitlab_project.id),
                    ),
                    Integration(
                        project_id=db_project.id,
                        name=IntegrationEnum.INFISICAL,
                        external_id=infisical_project.id,
                    ),
                    Integration(
                        project_id=db_project.id,
                        name=IntegrationEnum.LOGFIRE,
                        external_id=str(logfire_project.id),
                    ),
                    Integration(
                        project_id=db_project.id,
                        name=IntegrationEnum.JIRA,
                        external_id=str(jira_project.id),
                    ),
                ]
            )

            return ProjectCreated(repo_url=gitlab_project.ssh_url_to_repo, project_id=db_project.id)

        except (InfisicalError, LogfireError, SonarQubeError, JiraError) as e:
            logfire.error("Project creation failed, rolling back: {error}", error=str(e))
            await self._rollback_project_creation(
                gitlab_project_id=gitlab_project.id,
                gitlab_full_path=gitlab_project.path_with_namespace,
                project_key=project_key if sonarqube_created else None,
                jira_project_key=jira_project.key if jira_project else None,
                logfire_project_id=str(logfire_project.id) if logfire_project else None,
                infisical_project_id=infisical_project.id if infisical_project else None,
            )
            raise

    async def _rollback_project_creation(
        self,
        gitlab_project_id: int,
        gitlab_full_path: str,
        project_key: str | None = None,
        jira_project_key: str | None = None,
        logfire_project_id: str | None = None,
        infisical_project_id: str | None = None,
    ) -> None:
        try:
            await self.gitlab.delete_project(project_id=gitlab_project_id, full_path=gitlab_full_path)
        except GitLabError:
            logfire.error("Failed to rollback GitLab project {id}", id=gitlab_project_id)

        if project_key:
            try:
                await self.sonarqube.delete_project(project_key=project_key)
            except SonarQubeError:
                logfire.error("Failed to rollback SonarQube project {key}", key=project_key)

        if logfire_project_id:
            try:
                await self.logfire.delete_project(project_id=logfire_project_id)
            except LogfireError:
                logfire.error("Failed to rollback Logfire project {id}", id=logfire_project_id)

        if infisical_project_id:
            try:
                await self.infisical.delete_project(project_id=infisical_project_id)
            except InfisicalError:
                logfire.error("Failed to rollback Infisical project {id}", id=infisical_project_id)

        if jira_project_key:
            try:
                await self.jira.delete_project(project_key=jira_project_key)
            except JiraError:
                logfire.error("Failed to rollback Jira project {key}", key=jira_project_key)

    async def _setup_gitlab_project(self, project: ProjectDetail, project_key: str) -> GitLabProject:
        gitlab_project: GitLabProject = await self.gitlab.create_project(
            name=project.name,
            visibility="private",
            initialize_with_readme=False,
        )

        logfire_url: str = f"{self.logfire.base_url}Guty04/{logfire_slug(project.name)}"

        files: dict[str, str] = self.template_builder.build(
            data=BuilderProjectData(
                project_name=project.name,
                project_key=project_key,
                description=project.description,
                url_repository=gitlab_project.ssh_url_to_repo,
                codeowners=project.members,
                logfire_url=logfire_url,
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

        await self.gitlab.create_branch(
            project_id=gitlab_project.id,
            branch_name="release",
            from_branch="develop",
        )

        await self._protect_branches(project_id=gitlab_project.id)

        await self._add_members(project_id=gitlab_project.id, members=project.members)

        return gitlab_project

    async def _setup_sonarqube_project(
        self, project_key: str, project_name: str, gitlab_project_id: int
    ) -> SonarQubeToken:
        await self.sonarqube.set_gitlab_binding(
            project_name=project_name,
            project_key=project_key,
            gitlab_project_id=gitlab_project_id,
        )
        return await self.sonarqube.generate_project_token(
            project_key=project_key,
            token_name=f"{project_key}-token",
        )

    async def _setup_envs(
        self,
        infisical_project_id: str,
        logfire_project_id: UUID,
    ) -> None:
        logfire_write_token: LogfireWriteToken = await self.logfire.create_write_token(
            project_id=str(logfire_project_id)
        )

        secrets_data: dict[str, str] = {
            "JWT_ALGORITHM": "HS256",
            "SECRET_KEY": secrets.token_urlsafe(32),
            "ENVIRONMENT": "local",
            "LOGFIRE_TOKEN": logfire_write_token.token,
        }

        for key, value in secrets_data.items():
            await self.infisical.create_secret(
                project_id=infisical_project_id,
                environment="Local",
                secret_key=key,
                secret_value=value,
            )

    async def _setup_logfire_project(self, project_name: str, description: str) -> LogfireProject:
        logfire_project: LogfireProject = await self.logfire.create_project(
            project_name=logfire_slug(project_name),
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

    async def _setup_infisical_project(
        self,
        project_name: str,
        project_description: str,
    ) -> InfisicalProject:
        infisical_project: InfisicalProject = await self.infisical.create_project(
            project_name=f"{project_name} secrets",
            project_description=project_description,
        )
        infisical_project_id: str = infisical_project.id

        await self.infisical.create_environment(
            project_id=infisical_project_id,
            name="Local",
            slug="local",
            position=1,
        )

        identity_id: str = await self.infisical.create_identity(
            name=f"developers-{project_name}-identity",
            project_id=infisical_project_id,
        )

        client_secret: str = await self.infisical.create_client_secret(identity_id=identity_id, description="")

        client_id: str = await self.infisical.get_client_id(identity_id=identity_id)

        # TODO: Ya pensaremos como hacer llegar esto a los devs
        # TODO: Falta agregar permisos para que el TL pueda acceder
        # a la instancia de infisical y configurar todas las envs
        logfire.info("Infisical credentials", client_id=client_id, client_secret=client_secret)

        await self.infisical.attach_identity_to_project(
            identity_id=identity_id,
            project_id=infisical_project_id,
            role="viewer",
        )

        return infisical_project

    async def _setup_jira_project(self, project_key: str, project_name: str, project_description: str) -> JiraProject:
        unique_key: str = await self._generate_unique_project_key(project_key)
        return await self.jira.create_project(
            project_name=project_name,
            description=project_description,
            project_key=unique_key,
        )

    async def _generate_unique_project_key(self, base_key: str) -> str:
        projects: list[Project] = await self.repository.list_all_projects()
        used_keys: set[str] = {slugify(project.name) for project in projects}

        if base_key not in used_keys:
            return base_key

        for counter in range(1, 100):
            suffix: str = str(counter)
            candidate: str = base_key[: 10 - len(suffix)] + suffix
            if candidate not in used_keys:
                return candidate

        raise JiraError(f"Unable to generate unique project key for '{base_key}'")

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
        project: Project | None = await self.repository.get_by_id(project_id=project_id)

        if not project or project.id_user != user_id:
            raise ProjectNotFoundError()

        integration: Integration | None = await self.integration_repository.get_by_project_id(
            project_id=project.id, integration=IntegrationEnum.GITLAB
        )

        if not integration:
            raise ProjectNotFoundError()

        project_key: str = slugify(project.name)
        quality_gate: QualityGateStatus = await self.sonarqube.get_quality_gate_status(project_key=project_key)
        members: list[GitLabMember] = await self.gitlab.list_project_members(project_id=int(integration.external_id))
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
        projects: list[Project] = await self.repository.list_by_user(user_id=user_id)
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
        projects: list[Project] = await self.repository.list_all_projects()
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

        for branch in ("release", "hotfix/*"):
            await self.gitlab.protect_branch(
                project_id=project_id,
                branch_name=branch,
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
