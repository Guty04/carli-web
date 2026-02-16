from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Integration
from src.database.models.project import Project
from src.enums import Integration as IntegrationEnum


@dataclass
class IntegrationRepository:
    session: AsyncSession

    async def get_by_project_id(self, project_id: UUID, integration: IntegrationEnum) -> Integration | None:
        statement: Select[tuple[Integration]] = (
            select(Integration).join(Project).where(Integration.name == integration, Project.id == project_id)
        )

        result: Result[tuple[Integration]] = await self.session.execute(statement)

        return result.scalar_one_or_none()
