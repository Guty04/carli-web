from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.integration import Integration
from src.database.models.project import Project
from src.enums import Integration as IntegrationEnum


@dataclass
class ProjectRepository:
    session: AsyncSession

    async def create(
        self, name: str, id_user: UUID, url_repository: str, description: str, integrations: list[Integration]
    ) -> Project:
        project = Project(
            name=name,
            description=description,
            id_user=id_user,
            url_repository=url_repository,
        )
        project.integrations.update(integrations)
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

    async def get_by_integration_id(self, integration: IntegrationEnum, external_id: str) -> Project | None:
        statement: Select[tuple[Project]] = (
            select(Project)
            .join(Integration)
            .where(
                Integration.name == integration.value,
                Integration.external_id == external_id,
            )
        )
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
