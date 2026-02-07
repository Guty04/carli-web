from dataclasses import dataclass

from src.integrations.gemini import JiraTicketContent, TicketAgent
from src.integrations.jira import JiraClient, JiraIssue
from src.schemas import LogfireAlert


@dataclass
class WebhookService:
    jira: JiraClient
    jira_project_key: str
    ticket_agent: TicketAgent

    async def handle_logfire_alert(self, alert: LogfireAlert) -> JiraIssue:
        content: JiraTicketContent = await self.ticket_agent.analyze_alert(alert)

        return await self.jira.create_issue(
            project_key=self.jira_project_key,
            summary=content.summary,
            description=content.description,
        )
