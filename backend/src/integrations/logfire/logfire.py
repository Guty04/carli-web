from dataclasses import dataclass
from urllib.parse import urljoin

from httpx import AsyncClient, HTTPStatusError, RequestError, Response

from src.errors.logfire import (
    LogfireAPIError,
    LogfireAuthenticationError,
    LogfireError,
)

from .schemas import LogfireAlertConfiguration, LogfireChannel, LogfireProject, LogfireWriteToken

ERROR_ALERT_QUERY: str = (
    "SELECT project_id, "
    "trace_id,"
    "message,"
    "attributes -> 'fastapi.arguments.values' as request,"
    "exception_message,"
    "otel_events -> 0 ->'attributes'->>'exception.stacktrace' as stack_trace "
    "FROM records WHERE level = 'error'"
)


@dataclass
class LogfireClient:
    base_url: str
    token: str
    timeout: int = 30

    async def create_project(
        self,
        project_name: str,
        description: str = "",
        visibility: str = "private",
    ) -> LogfireProject:
        url: str = urljoin(base=self.base_url, url="v1/projects/")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={
                        "project_name": project_name,
                        "description": description,
                        "visibility": visibility,
                    },
                    headers=self._headers(),
                )

                response.raise_for_status()

                return LogfireProject.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise LogfireAPIError(f"Request failed: {e!s}") from e

    async def create_write_token(self, project_id: str) -> LogfireWriteToken:
        url: str = urljoin(
            base=self.base_url,
            url=f"v1/projects/{project_id}/write-tokens/",
        )

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    headers=self._headers(),
                )

                response.raise_for_status()

                return LogfireWriteToken.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise LogfireAPIError(f"Request failed: {e!s}") from e

    async def create_channel(
        self,
        label: str,
        webhook_url: str,
    ) -> LogfireChannel:
        url: str = urljoin(base=self.base_url, url="v1/channels/")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={"label": label, "config": {"type": "webhook", "format": "raw-data", "url": webhook_url}},
                    headers=self._headers(),
                )

                response.raise_for_status()

                return LogfireChannel.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise LogfireAPIError(f"Request failed: {e!s}") from e

    async def create_alert(
        self,
        project_id: str,
        name: str,
        description: str,
        query: str,
        channel_ids: list[str],
        time_window: str = "PT5M",
        frequency: str = "PT1M",
        watermark: str = "PT0S",
    ) -> LogfireAlertConfiguration:
        url: str = urljoin(
            base=self.base_url,
            url=f"v1/projects/{project_id}/alerts/",
        )

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={
                        "name": name,
                        "description": description,
                        "query": query,
                        "time_window": time_window,
                        "frequency": frequency,
                        "watermark": watermark,
                        "channel_ids": channel_ids,
                        "notify_when": "has_matches",
                    },
                    headers=self._headers(),
                )

                response.raise_for_status()

                return LogfireAlertConfiguration.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise LogfireAPIError(f"Request failed: {e!s}") from e

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    @staticmethod
    def _handle_http_error(error: HTTPStatusError) -> LogfireError:
        if error.response.status_code == 401:
            return LogfireAuthenticationError()

        return LogfireAPIError()
