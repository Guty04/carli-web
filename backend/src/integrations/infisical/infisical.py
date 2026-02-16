from dataclasses import dataclass
from urllib.parse import urljoin

from httpx import AsyncClient, HTTPStatusError, RequestError, Response

from src.errors import (
    InfisicalAPIError,
    InfisicalAuthenticationError,
    InfisicalError,
)

from .schemas import InfisicalProject


@dataclass
class InfisicalClient:
    base_url: str
    client_id: str
    client_secret: str
    token: str | None = None
    timeout: int = 30

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    @staticmethod
    def _handle_http_error(error: HTTPStatusError) -> InfisicalError:
        if error.response.status_code == 401:
            return InfisicalAuthenticationError()
        if error.response.status_code == 404:
            return InfisicalAPIError("Resource not found")
        return InfisicalAPIError(f"HTTP {error.response.status_code}")

    async def get_token(self) -> str:
        url: str = urljoin(self.base_url, "api/v1/auth/universal-auth/login")

        headers: dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url, headers=headers, data={"clientId": self.client_id, "clientSecret": self.client_secret}
                )
                response.raise_for_status()

                access_token = response.json()["accessToken"]

                self.token = access_token

                return access_token

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise InfisicalAPIError(f"Request failed: {str(e)}") from e

    async def create_project(
        self,
        project_name: str,
        project_description: str,
    ) -> InfisicalProject:
        url: str = urljoin(self.base_url, "api/v2/workspace")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={
                        "projectName": project_name,
                        "projectDescription": project_description,
                        "type": "secret-manager",
                        "shouldCreateDefaultEnvs": True,
                        "hasDeleteProtection": True,
                    },
                    headers=self._headers(),
                )
                response.raise_for_status()
                return InfisicalProject.model_validate(response.json()["project"])

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e
        except RequestError as e:
            raise InfisicalAPIError(f"Request failed: {str(e)}") from e

    async def create_environment(
        self,
        project_id: str,
        name: str,
        slug: str,
        position: int = 1,
    ) -> None:
        url: str = urljoin(self.base_url, f"api/v1/projects/{project_id}/environments")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={"name": name, "slug": slug, "position": position},
                    headers=self._headers(),
                )
                response.raise_for_status()

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e
        except RequestError as e:
            raise InfisicalAPIError(f"Request failed: {str(e)}") from e

    async def create_identity(
        self,
        name: str,
        project_id: str,
    ) -> str:
        url: str = urljoin(self.base_url, f"api/v1/projects/{project_id}/identities")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={"name": name},
                    headers=self._headers(),
                )
                response.raise_for_status()
                return response.json()["identity"]["id"]

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e
        except RequestError as e:
            raise InfisicalAPIError(f"Request failed: {str(e)}") from e

    async def create_client_secret(self, identity_id: str, description: str) -> str:
        url: str = urljoin(
            self.base_url,
            f"api/v1/auth/universal-auth/identities/{identity_id}/client-secrets",
        )

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={
                        "description": description,
                        "numUsesLimit": 0,
                    },
                    headers=self._headers(),
                )
                response.raise_for_status()
                return response.json()["clientSecret"]

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e
        except RequestError as e:
            raise InfisicalAPIError(f"Request failed: {str(e)}") from e

    async def get_client_id(self, identity_id: str) -> str:
        url: str = urljoin(
            self.base_url,
            f"api/v1/auth/universal-auth/identities/{identity_id}",
        )

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.get(
                    url=url,
                    headers=self._headers(),
                )
                response.raise_for_status()

                return response.json()["identityUniversalAuth"]["clientId"]

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e
        except RequestError as e:
            raise InfisicalAPIError(f"Request failed: {str(e)}") from e

    async def attach_identity_to_project(
        self,
        identity_id: str,
        project_id: str,
        role: str = "viewer",
    ) -> None:
        url: str = urljoin(
            self.base_url,
            f"api/v1/projects/{project_id}/identity-memberships/{identity_id}",
        )

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={"role": role},
                    headers=self._headers(),
                )
                response.raise_for_status()

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e
        except RequestError as e:
            raise InfisicalAPIError(f"Request failed: {str(e)}") from e

    async def create_secret(
        self,
        project_id: str,
        environment: str,
        secret_key: str,
        secret_value: str,
        secret_path: str = "/",  # noqa: S107
    ) -> None:
        url: str = urljoin(self.base_url, f"api/v3/secrets/raw/{secret_key}")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={
                        "workspaceId": project_id,
                        "environment": environment,
                        "secretPath": secret_path,
                        "secretValue": secret_value,
                    },
                    headers=self._headers(),
                )
                response.raise_for_status()

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e
        except RequestError as e:
            raise InfisicalAPIError(f"Request failed: {str(e)}") from e

    async def delete_project(self, project_id: str) -> None:
        url = urljoin(self.base_url, f"api/v1/projects/{project_id}")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.delete(
                    url=url,
                    headers=self._headers(),
                )
                response.raise_for_status()

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e
        except RequestError as e:
            raise InfisicalAPIError(f"Request failed: {str(e)}") from e
