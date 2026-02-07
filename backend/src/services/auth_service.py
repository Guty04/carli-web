from dataclasses import dataclass
from typing import Any
from uuid import UUID

from jwt import InvalidTokenError

from src.database.models import User
from src.errors import AuthenticationError, AuthorizationError
from src.repositories import AuthRepository
from src.schemas import Token, TokenPayload
from src.utils import create_access_token, decode_access_token, verify_password


@dataclass
class AuthService:
    repository: AuthRepository

    async def login(self, email: str, password: str) -> Token:
        user: User | None = await self.repository.get_user_by_email(email=email)

        if user is None or not verify_password(plain=password, hashed=user.password):
            raise AuthenticationError()

        access_token: str = create_access_token(TokenPayload(sub=str(user.id)))

        return Token(access_token=access_token)

    async def get_current_user(self, access_token: str, required_scopes: set[str]) -> User:
        try:
            payload: dict[str, Any] = decode_access_token(token=access_token)
        except InvalidTokenError as token_error:
            raise AuthenticationError() from token_error

        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise AuthenticationError()

        user: User | None = await self.repository.get_user_by_id(UUID(user_id))
        if user is None:
            raise AuthenticationError()

        user_permissions: set[str] = {permission.name for permission in user.role.permissions}

        if not required_scopes.issubset(user_permissions):
            raise AuthorizationError()

        return user
