from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"  # noqa: S105


class TokenPayload(BaseModel):
    sub: str
    name: str
    role: str
