from dataclasses import dataclass

from src.database.models import Project
from src.integrations.gemini import JiraTicketContent, TicketAgent
from src.integrations.jira import JiraClient
from src.repositories import ProjectRepository
from src.schemas import LogfireAlert


@dataclass
class WebhookService:
    jira: JiraClient
    repository: ProjectRepository
    ticket_agent: TicketAgent

    async def handle_logfire_alert(self, alert: LogfireAlert) -> None:
        project: Project | None = await self.repository.get_by_logfire_id(logfire_id=alert.project_id)

        if project is None:
            return

        content: JiraTicketContent = await self.ticket_agent.analyze_alert(alert=alert)

        await self.jira.create_issue(
            project_id=project.id_project_jira,
            summary=content.summary,
            description=content.description,
        )
