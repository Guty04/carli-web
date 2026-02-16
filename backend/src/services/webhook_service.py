from dataclasses import dataclass

from src.database.models import Integration, Project
from src.enums import Integration as IntegrationEnum
from src.integrations.gemini import JiraTicketContent, TicketAgent
from src.integrations.jira import JiraClient
from src.repositories import IntegrationRepository, ProjectRepository
from src.schemas import LogfireAlert


@dataclass
class WebhookService:
    jira: JiraClient
    repository: ProjectRepository
    integration_repository: IntegrationRepository
    ticket_agent: TicketAgent

    async def handle_logfire_alert(self, alert: LogfireAlert) -> None:
        project: Project | None = await self.repository.get_by_integration_id(
            integration=IntegrationEnum.LOGFIRE, external_id=str(alert.project_id)
        )

        if project is None:
            return

        jira_integration: Integration | None = await self.integration_repository.get_by_project_id(
            project_id=project.id, integration=IntegrationEnum.JIRA
        )

        if not jira_integration:
            return

        content: JiraTicketContent = await self.ticket_agent.analyze_alert(alert=alert)

        await self.jira.create_issue(
            project_id=int(jira_integration.external_id),
            summary=content.summary,
            description=content.description,
        )
