from dataclasses import dataclass
from typing import Tuple
from uuid import UUID

from sqlalchemy import Result, select
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
    ) -> Project:
        project = Project(
            name=name,
            id_user=id_user,
            id_project_gitlab=id_project_gitlab,
            url_repository=url_repository,
        )
        self.session.add(project)
        await self.session.flush()
        return project

    async def get_by_id(self, project_id: UUID) -> Project | None:
        result: Result[Tuple[Project]] = await self.session.execute(
            statement=select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: UUID) -> list[Project]:
        result: Result[Tuple[Project]] = await self.session.execute(
            statement=select(Project).where(Project.id_user == user_id)
        )
        return list(result.scalars().all())

    async def list_all_repositories(self) -> list[Project]:
        result: Result[Tuple[Project]] = await self.session.execute(
            statement=select(Project)
        )
        return list(result.scalars().all())
