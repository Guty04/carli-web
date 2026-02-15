from dataclasses import dataclass

from src.integrations import GitLabClient
from src.schemas.user import UserSummary


@dataclass
class UserService:
    gitlab: GitLabClient

    async def list_all_users(self) -> list[UserSummary]:
        users = await self.gitlab.list_all_users()
        return [
            UserSummary(
                id=user.id,
                username=user.username,
                name=user.name,
                avatar_url=user.avatar_url,
            )
            for user in users
        ]
