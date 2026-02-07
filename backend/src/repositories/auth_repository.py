from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Role, User


@dataclass
class AuthRepository:
    session: AsyncSession

    async def get_user_by_email(self, email: str) -> User | None:
        statement: Select[tuple[User]] = (
            select(User).options(selectinload(User.role).selectinload(Role.permissions))
        ).where(User.email == email)

        result: Result[tuple[User]] = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.session.get(User, user_id)
