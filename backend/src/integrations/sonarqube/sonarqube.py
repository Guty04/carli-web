from base64 import b64encode
from dataclasses import dataclass
from urllib.parse import urljoin

from httpx import AsyncClient, HTTPStatusError, RequestError, Response

from src.errors.sonarqube import (
    SonarQubeAPIError,
    SonarQubeAuthenticationError,
    SonarQubeError,
    SonarQubeNotFoundError,
)

from .schemas import SonarQubeProject, SonarQubeToken


@dataclass
class SonarQubeClient:
    base_url: str
    token: str
    timeout: int = 30

    async def create_project(
        self,
        project_name: str,
        project_key: str,
        visibility: str = "private",
    ) -> SonarQubeProject:
        url: str = urljoin(base=self.base_url, url="api/projects/create")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    params={
                        "name": project_name,
                        "project": project_key,
                        "visibility": visibility,
                    },
                    headers=self._headers(),
                )

                response.raise_for_status()

                return SonarQubeProject.model_validate(response.json()["project"])

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise SonarQubeAPIError(f"Request failed: {str(e)}") from e

    async def generate_project_token(
        self,
        project_key: str,
        token_name: str,
    ) -> SonarQubeToken:
        url: str = urljoin(base=self.base_url, url="api/user_tokens/generate")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    params={
                        "name": token_name,
                        "projectKey": project_key,
                        "type": "PROJECT_ANALYSIS_TOKEN",
                    },
                    headers=self._headers(),
                )

                response.raise_for_status()

                return SonarQubeToken.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise SonarQubeAPIError(f"Request failed: {str(e)}") from e

    def _headers(self) -> dict[str, str]:
        credentials: str = b64encode(f"{self.token}:".encode()).decode()
        return {"Authorization": f"Basic {credentials}"}

    @staticmethod
    def _handle_http_error(error: HTTPStatusError) -> SonarQubeError:
        if error.response.status_code == 401:
            return SonarQubeAuthenticationError()

        elif error.response.status_code == 404:
            return SonarQubeNotFoundError()

        else:
            return SonarQubeAPIError()
