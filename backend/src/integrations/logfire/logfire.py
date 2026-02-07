from dataclasses import dataclass
from urllib.parse import urljoin

from httpx import AsyncClient, HTTPStatusError, RequestError, Response

from src.errors.logfire import (
    LogfireAPIError,
    LogfireAuthenticationError,
    LogfireError,
)

from .schemas import LogfireProject, LogfireWriteToken


@dataclass
class LogfireClient:
    base_url: str
    token: str
    timeout: int = 30

    async def create_project(
        self,
        project_name: str,
        visibility: str = "private",
    ) -> LogfireProject:
        url: str = urljoin(base=self.base_url, url="api/v1/projects/")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={
                        "project_name": project_name,
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
            url=f"api/v1/projects/{project_id}/write-tokens/",
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

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    @staticmethod
    def _handle_http_error(error: HTTPStatusError) -> LogfireError:
        if error.response.status_code == 401:
            return LogfireAuthenticationError()

        return LogfireAPIError()
