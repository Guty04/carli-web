from dataclasses import dataclass

from src.database.models import User
from src.errors import AuthenticationError
from src.repositories import AuthRepository
from src.schemas import Token, TokenPayload
from src.utils import create_access_token, verify_password


@dataclass
class AuthService:
    repository: AuthRepository

    async def login(self, email: str, password: str) -> Token:
        user: User | None = await self.repository.get_user_by_email(email=email)

        if user is None or not verify_password(plain=password, hashed=user.password):
            raise AuthenticationError()

        access_token: str = create_access_token(TokenPayload(sub=str(user.id)))

        return Token(access_token=access_token)
