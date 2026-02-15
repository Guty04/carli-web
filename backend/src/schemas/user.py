from pydantic import BaseModel


class UserSummary(BaseModel):
    id: int
    username: str
    name: str
    avatar_url: str | None = None
