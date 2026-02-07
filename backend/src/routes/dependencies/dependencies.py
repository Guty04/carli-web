from pathlib import Path

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.ext.asyncio import AsyncSession

from src.builders import BackendBuilder
from src.configurations import configuration
from src.database import database
from src.database.models import User
from src.errors import AuthenticationError, AuthorizationError
from src.integrations import GitLabClient, JiraClient, LogfireClient, SonarQubeClient, TicketAgent
from src.repositories import AuthRepository, ProjectRepository
from src.services import AuthService, ProjectService, WebhookService
from src.utils.template_generator import TemplateGenerator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_auth_service(
    session: AsyncSession = Depends(dependency=database.get_async_session),
) -> AuthService:
    return AuthService(repository=AuthRepository(session=session))


async def get_current_user(
    security: SecurityScopes,
    auth_service: AuthService = Depends(dependency=get_auth_service),
    access_token: str = Depends(dependency=oauth2_scheme),
) -> User:
    try:
        return await auth_service.get_current_user(
            access_token=access_token,
            required_scopes=set(security.scopes),
        )
    except AuthenticationError as auth_error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from auth_error

    except AuthorizationError as permissions_error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        ) from permissions_error


def get_gitlab_client() -> GitLabClient:
    return GitLabClient(
        base_url=f"{configuration.GITLAB_API_URL}api/v4/",
        private_token=configuration.GITLAB_PRIVATE_TOKEN,
        gitlab_namespace_id=configuration.GITLAB_NAMESPACE_ID,
    )


def get_sonarqube_client() -> SonarQubeClient:
    return SonarQubeClient(
        base_url=f"{configuration.SONARQUBE_API_URL}",
        token=configuration.SONARQUBE_TOKEN,
    )


def get_logfire_client() -> LogfireClient:
    return LogfireClient(
        base_url=f"{configuration.LOGFIRE_API_URL}",
        token=configuration.LOGFIRE_TOKEN,
    )


def get_backend_builder() -> BackendBuilder:
    templates_directory: Path = Path(__file__).parent.parent.parent / "templates"
    template_generator = TemplateGenerator(templates_directory=templates_directory)
    return BackendBuilder(template_generator=template_generator)


def get_jira_client() -> JiraClient:
    return JiraClient(
        base_url=f"{configuration.JIRA_API_URL}",
        user_email=configuration.JIRA_USER_EMAIL,
        token=configuration.JIRA_TOKEN,
    )


def get_ticket_agent() -> TicketAgent:
    return TicketAgent(api_key=configuration.GEMINI_API_KEY, model_name=configuration.GEMINI_MODEL)


def get_webhook_service(
    jira_client: JiraClient = Depends(dependency=get_jira_client),
    ticket_agent: TicketAgent = Depends(dependency=get_ticket_agent),
) -> WebhookService:
    return WebhookService(
        jira=jira_client,
        jira_project_key=configuration.JIRA_PROJECT_KEY,
        ticket_agent=ticket_agent,
    )


def get_project_service(
    session: AsyncSession = Depends(dependency=database.get_async_session),
    gitlab_client: GitLabClient = Depends(dependency=get_gitlab_client),
    sonarqube_client: SonarQubeClient = Depends(dependency=get_sonarqube_client),
    logfire_client: LogfireClient = Depends(dependency=get_logfire_client),
    backend_builder: BackendBuilder = Depends(dependency=get_backend_builder),
) -> ProjectService:
    return ProjectService(
        gitlab=gitlab_client,
        sonarqube=sonarqube_client,
        logfire=logfire_client,
        repository=ProjectRepository(session=session),
        template_builder=backend_builder,
        webhook_base_url=str(configuration.WEBHOOK_BASE_URL),
    )
