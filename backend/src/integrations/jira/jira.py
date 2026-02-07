from base64 import b64encode
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

from httpx import AsyncClient, HTTPStatusError, RequestError, Response

from src.errors.jira import JiraAPIError, JiraAuthenticationError, JiraError

from .schemas import JiraIssue


@dataclass
class JiraClient:
    base_url: str
    user_email: str
    token: str
    timeout: int = 30

    async def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Bug",
    ) -> JiraIssue:
        url: str = urljoin(base=self.base_url, url="rest/api/3/issue")

        payload: dict[str, Any] = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": description},
                            ],
                        },
                    ],
                },
                "issuetype": {"name": issue_type},
            },
        }

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json=payload,
                    headers=self._headers(),
                )

                response.raise_for_status()

                return JiraIssue.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise JiraAPIError(f"Request failed: {e!s}") from e

    def _headers(self) -> dict[str, str]:
        credentials: str = b64encode(
            f"{self.user_email}:{self.token}".encode(),
        ).decode()
        return {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _handle_http_error(error: HTTPStatusError) -> JiraError:
        if error.response.status_code == 401:
            return JiraAuthenticationError()

        return JiraAPIError()
