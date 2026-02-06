from typing import Any
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations import configuration
from src.database import database
from src.database.models import User
from src.errors import AuthorizationError
from src.integrations import GitLabClient
from src.repositories import AuthRepository, ProjectRepository
from src.services import AuthService, ProjectService
from src.utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_auth_service(
    session: AsyncSession = Depends(dependency=database.get_async_session),
) -> AuthService:
    return AuthService(repository=AuthRepository(session=session))


async def get_current_user(
    security: SecurityScopes,
    session: AsyncSession = Depends(database.get_async_session),
    access_token: str = Depends(dependency=oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, Any] = decode_access_token(token=access_token)
    except InvalidTokenError:
        raise credentials_exception

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    repository: AuthRepository = AuthRepository(session=session)
    user: User | None = await repository.get_user_by_id(UUID(user_id))

    if user is None:
        raise credentials_exception

    user_permissions: set[str] = {
        permission.name for permission in user.role.permissions
    }

    if not set(security.scopes).issubset(user_permissions):
        raise AuthorizationError()

    return user


def get_gitlab_client() -> GitLabClient:
    return GitLabClient(
        base_url=f"{configuration.GITLAB_API_URL}api/v4/",
        private_token=configuration.GITLAB_PRIVATE_TOKEN,
    )


def get_project_service(
    session: AsyncSession = Depends(dependency=database.get_async_session),
    gitlab_client: GitLabClient = Depends(dependency=get_gitlab_client),
) -> ProjectService:
    return ProjectService(
        gitlab=gitlab_client,
        repository=ProjectRepository(session=session),
    )
