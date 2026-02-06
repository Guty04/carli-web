from dataclasses import dataclass
from uuid import UUID

from src.database.models import Project
from src.integrations.gitlab import AccessLevel, GitLabClient
from src.integrations.gitlab.schemas import GitLabProject
from src.repositories import ProjectRepository
from src.schemas import Member, ProjectCreated, ProjectDetail, ProjectSummary

ROLE_TO_ACCESS_LEVEL: dict[str, AccessLevel] = {
    "developer": AccessLevel.DEVELOPER,
    "maintainer": AccessLevel.MAINTAINER,
    "reporter": AccessLevel.REPORTER,
}


@dataclass
class ProjectService:
    gitlab: GitLabClient
    repository: ProjectRepository

    async def create_project(
        self, project: ProjectDetail, user_id: UUID
    ) -> ProjectCreated:
        gitlab_project: GitLabProject = await self.gitlab.create_project(
            name=project.name,
            namespace_id=self._get_namespace_id(),
            visibility="private",
            initialize_with_readme=False,
        )

        # TODO: build template files and initial commit via TemplateFileBuilder

        await self.gitlab.create_branch(
            project_id=gitlab_project.id,
            branch_name="develop",
            from_branch="main",
        )

        await self._protect_branches(gitlab_project.id)

        await self.gitlab.configure_merge_request_approvals(gitlab_project.id)

        await self._add_members(gitlab_project.id, project.members)

        db_project: Project = await self.repository.create(
            name=project.name,
            id_user=user_id,
            id_project_gitlab=gitlab_project.id,
            url_repository=gitlab_project.ssh_url_to_repo,
        )

        return ProjectCreated(
            repo_url=gitlab_project.ssh_url_to_repo, project_id=db_project.id
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

    async def _protect_branches(self, project_id: int) -> None:
        await self.gitlab.protect_branch(
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
            access_level: AccessLevel = ROLE_TO_ACCESS_LEVEL.get(
                member.role.lower(), AccessLevel.DEVELOPER
            )
            await self.gitlab.add_member_to_project(
                project_id=project_id,
                user_id=member.gitlab_user_id,
                access_level=access_level,
            )

    def _get_namespace_id(self) -> int:
        from src.configurations import configuration

        return configuration.GITLAB_NAMESPACE_ID
