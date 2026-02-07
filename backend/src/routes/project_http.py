from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Security, status

from src.database.models import User
from src.enums import Permission
from src.errors import GitLabError, LogfireError, ProjectNotFoundError, SonarQubeError
from src.schemas import ProjectCreated, ProjectDetail, ProjectOverview, ProjectSummary
from src.services import ProjectService

from .dependencies import get_current_user, get_project_service

project_router: APIRouter = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.post(path="/", response_model=ProjectCreated, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectDetail,
    current_user: User = Security(dependency=get_current_user, scopes=[Permission.CREATE_PROJECT]),
    project_service: ProjectService = Depends(dependency=get_project_service),
) -> ProjectCreated:
    try:
        return await project_service.create_project(project=project, user_id=current_user.id)

    except (GitLabError, LogfireError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@project_router.get(path="/", response_model=list[ProjectSummary])
async def list_projects(
    current_user: User = Security(dependency=get_current_user, scopes=[Permission.READ_PROJECTS]),
    project_service: ProjectService = Depends(dependency=get_project_service),
) -> list[ProjectSummary]:
    return await project_service.list_projects(user_id=current_user.id)


@project_router.get(path="/{project_id}", response_model=ProjectOverview)
async def get_project(
    project_id: str,
    current_user: User = Security(dependency=get_current_user, scopes=[Permission.READ_PROJECTS]),
    project_service: ProjectService = Depends(dependency=get_project_service),
) -> ProjectOverview:
    try:
        return await project_service.get_project_overview(user_id=current_user.id, project_id=UUID(project_id))

    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except (GitLabError, SonarQubeError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
