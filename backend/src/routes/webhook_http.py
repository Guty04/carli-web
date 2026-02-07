from fastapi import APIRouter, Depends, HTTPException, status

from src.errors import GeminiError, JiraError
from src.schemas import LogfireAlert
from src.services import WebhookService

from .dependencies import get_webhook_service

webhook_router: APIRouter = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@webhook_router.post(
    path="/logfire/alerts",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def handle_logfire_alert(
    alert: LogfireAlert,
    webhook_service: WebhookService = Depends(dependency=get_webhook_service),
) -> None:
    try:
        await webhook_service.handle_logfire_alert(alert=alert)

    except (JiraError, GeminiError) as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        ) from e
