from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.project import Project


@dataclass
class ProjectRepository:
    session: AsyncSession

    async def create(
        self,
        name: str,
        id_user: UUID,
        id_project_gitlab: int,
        url_repository: str,
        description: str,
        id_project_logfire: str,
        id_project_jira: int,
    ) -> Project:
        project = Project(
            name=name,
            description=description,
            id_user=id_user,
            id_project_gitlab=id_project_gitlab,
            url_repository=url_repository,
            id_project_logfire=id_project_logfire,
            id_project_jira=id_project_jira,
        )
        self.session.add(project)
        await self.session.flush()
        return project

    async def get_by_name(self, name: str) -> Project | None:
        result: Result[tuple[Project]] = await self.session.execute(
            statement=select(Project).where(Project.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, project_id: UUID) -> Project | None:
        result: Result[tuple[Project]] = await self.session.execute(
            statement=select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_by_logfire_id(self, logfire_id: UUID) -> Project | None:
        statement: Select[tuple[Project]] = select(Project).where(Project.id_project_logfire == logfire_id)
        result: Result[tuple[Project]] = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: UUID) -> list[Project]:
        result: Result[tuple[Project]] = await self.session.execute(
            statement=select(Project).where(Project.id_user == user_id)
        )
        return list(result.scalars().all())

    async def list_all_projects(self) -> list[Project]:
        result: Result[tuple[Project]] = await self.session.execute(statement=select(Project))
        return list(result.scalars().all())
