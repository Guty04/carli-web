from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from src.errors import AuthenticationError
from src.schemas import Token
from src.services import AuthService

from .dependencies import get_auth_service

auth_router: APIRouter = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model=Token)
async def login(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(dependency=get_auth_service),
) -> Token:
    try:
        token: Token = await auth_service.login(
            email=credentials.username, password=credentials.password
        )

    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e

    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return token


@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    response.delete_cookie(
        key="access_token", httponly=True, secure=True, samesite="lax"
    )
