from fastapi import APIRouter, Depends, HTTPException, Security, status

from src.database.models import User
from src.enums import Permission
from src.errors import GitLabError
from src.schemas.user import UserSummary
from src.services.user_service import UserService

from .dependencies import get_current_user, get_user_service

user_router: APIRouter = APIRouter(prefix="/users", tags=["Users"])


@user_router.get(path="/", response_model=list[UserSummary])
async def get_all_users(
    current_user: User = Security(dependency=get_current_user, scopes=[Permission.READ_USERS]),
    user_service: UserService = Depends(dependency=get_user_service),
) -> list[UserSummary]:
    try:
        return await user_service.list_all_users()

    except GitLabError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
