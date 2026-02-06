from dataclasses import dataclass
from typing import Tuple
from uuid import UUID

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.user import User


@dataclass
class AuthRepository:
    session: AsyncSession

    async def get_user_by_email(self, email: str) -> User | None:
        result: Result[Tuple[User]] = await self.session.execute(
            statement=select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        result: Result[Tuple[User]] = await self.session.execute(
            statement=select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
