from pydantic import BaseModel


class JiraTicketContent(BaseModel):
    summary: str
    description: str
