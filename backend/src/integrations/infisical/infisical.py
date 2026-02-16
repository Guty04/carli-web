import time
from dataclasses import dataclass, field
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
    _token_expires_at: float = field(default=0.0, init=False, repr=False)

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def _is_token_valid(self) -> bool:
        return self.token is not None and time.time() < self._token_expires_at

    async def _ensure_token(self) -> None:
        if not self._is_token_valid():
            await self._authenticate()

    @staticmethod
    def _handle_http_error(error: HTTPStatusError) -> InfisicalError:
        if error.response.status_code == 401:
            return InfisicalAuthenticationError()
        if error.response.status_code == 404:
            return InfisicalAPIError("Resource not found")
        return InfisicalAPIError(f"HTTP {error.response.status_code}")

    async def _authenticate(self) -> str:
        url: str = urljoin(self.base_url, "api/v1/auth/universal-auth/login")

        headers: dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url, headers=headers, data={"clientId": self.client_id, "clientSecret": self.client_secret}
                )
                response.raise_for_status()

                data = response.json()
                access_token: str = data["accessToken"]
                expires_in: int = data["expiresIn"]
                self.token = access_token
                self._token_expires_at = time.time() + expires_in - 30

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
        await self._ensure_token()
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
        await self._ensure_token()
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
        await self._ensure_token()
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

    async def configure_universal_auth(self, identity_id: str) -> str:
        await self._ensure_token()
        url: str = urljoin(
            self.base_url,
            f"api/v1/auth/universal-auth/identities/{identity_id}",
        )

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={
                        "clientSecretTrustedIps": [{"ipAddress": "0.0.0.0/0"}, {"ipAddress": "::/0"}],
                        "accessTokenTrustedIps": [{"ipAddress": "0.0.0.0/0"}, {"ipAddress": "::/0"}],
                        "accessTokenTTL": 2592000,
                        "accessTokenMaxTTL": 2592000,
                        "accessTokenNumUsesLimit": 0,
                        "accessTokenPeriod": 0,
                        "lockoutEnabled": True,
                        "lockoutThreshold": 3,
                        "lockoutDurationSeconds": 300,
                        "lockoutCounterResetSeconds": 30,
                    },
                    headers=self._headers(),
                )
                response.raise_for_status()
                return response.json()["identityUniversalAuth"]["clientId"]

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e
        except RequestError as e:
            raise InfisicalAPIError(f"Request failed: {str(e)}") from e

    async def create_client_secret(self, identity_id: str, description: str) -> str:
        await self._ensure_token()
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

    async def update_identity_membership(
        self,
        identity_id: str,
        project_id: str,
        role: str = "viewer",
    ) -> None:
        await self._ensure_token()
        url: str = urljoin(
            self.base_url,
            f"api/v1/projects/{project_id}/memberships/identities/{identity_id}",
        )

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.patch(
                    url=url,
                    json={"roles": [{"role": role, "isTemporary": False}]},
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
        secret_value: str | int,
        secret_path: str = "/",  # noqa: S107
    ) -> None:
        await self._ensure_token()
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
        await self._ensure_token()
        url: str = urljoin(self.base_url, f"api/v1/projects/{project_id}")

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
