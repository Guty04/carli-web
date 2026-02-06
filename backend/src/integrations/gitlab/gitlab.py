from dataclasses import dataclass
from urllib.parse import urljoin

from httpx import AsyncClient, HTTPStatusError, RequestError, Response

from src.errors import (
    GitLabAPIError,
    GitLabAuthenticationError,
    GitLabError,
    GitLabNotFoundError,
)

from .domain import AccessLevel
from .schemas import (
    GitLabApprovalConfiguration,
    GitLabBranch,
    GitLabCommit,
    GitLabMember,
    GitLabProject,
    GitLabProtectedBranch,
    GitLabUser,
)


@dataclass
class GitLabClient:
    base_url: str
    private_token: str
    timeout: int = 30

    async def create_project(
        self,
        name: str,
        namespace_id: int,
        visibility: str,
        initialize_with_readme: bool,
    ) -> GitLabProject:
        url: str = urljoin(base=self.base_url, url="projects")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url=url,
                    json={
                        "name": name,
                        "namespace_id": namespace_id,
                        "visibility": visibility,
                        "initialize_with_readme": initialize_with_readme,
                    },
                    headers=self._headers(),
                )

                response.raise_for_status()

                return GitLabProject.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise GitLabAPIError(f"Request failed: {str(e)}") from e

    async def create_branch(
        self, project_id: int, branch_name: str, from_branch: str
    ) -> GitLabBranch:
        url: str = urljoin(
            base=self.base_url, url=f"projects/{project_id}/repository/branches"
        )

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url,
                    params={"branch": branch_name, "ref": from_branch},
                    headers=self._headers(),
                )

                response.raise_for_status()

                return GitLabBranch.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise GitLabAPIError(f"Request failed: {str(e)}") from e

    async def protect_branch(
        self,
        project_id: int,
        branch_name: str,
        push_access_level: AccessLevel,
        merge_access_level: AccessLevel,
        allow_force_push: bool = False,
    ) -> GitLabProtectedBranch:
        url: str = urljoin(
            base=self.base_url, url=f"projects/{project_id}/protected_branches"
        )

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url,
                    json={
                        "name": branch_name,
                        "push_access_level": push_access_level.value,
                        "merge_access_level": merge_access_level.value,
                        "allow_force_push": allow_force_push,
                    },
                    headers=self._headers(),
                )

                response.raise_for_status()

                return GitLabProtectedBranch.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise GitLabAPIError(f"Request failed: {str(e)}") from e

    async def inicialize_repository(
        self,
        project_id: int,
        files: dict[str, str],
        commit_message: str,
    ) -> GitLabCommit:
        url: str = urljoin(
            base=self.base_url, url=f"projects/{project_id}/repository/commits"
        )

        actions: list[dict[str, str]] = [
            {
                "action": "create",
                "file_path": file_path,
                "content": content,
            }
            for file_path, content in files.items()
        ]

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url,
                    json={
                        "branch": "main",
                        "commit_message": commit_message,
                        "actions": actions,
                    },
                    headers=self._headers(),
                )

                response.raise_for_status()

                return GitLabCommit.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise GitLabAPIError(f"Request failed: {str(e)}") from e

    async def configure_merge_request_approvals(
        self,
        project_id: int,
    ) -> GitLabApprovalConfiguration:
        url: str = urljoin(base=self.base_url, url=f"projects/{project_id}/approvals")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url,
                    json={
                        "approvals_before_merge": 1,
                        "disable_overriding_approvers_per_merge_request": False,
                        "reset_approvals_on_push": True,
                        "merge_requests_author_approval": False,
                        "require_password_to_approve": False,
                    },
                    headers=self._headers(),
                )

                response.raise_for_status()

                return GitLabApprovalConfiguration.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise GitLabAPIError(f"Request failed: {str(e)}") from e

    async def add_member_to_project(
        self, project_id: int, user_name: str, access_level: AccessLevel
    ) -> GitLabMember:
        url: str = urljoin(self.base_url, f"projects/{project_id}/members")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.post(
                    url,
                    json={"user_name": user_name, "access_level": access_level.value},
                    headers=self._headers(),
                )

                response.raise_for_status()

                return GitLabMember.model_validate(response.json())

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise GitLabAPIError(f"Request failed: {str(e)}") from e

    async def search_users(self, search: str) -> list[GitLabUser]:
        url: str = urljoin(self.base_url, "users")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.get(
                    url,
                    params={"search": search},
                    headers=self._headers(),
                )

                response.raise_for_status()

                return [GitLabUser.model_validate(u) for u in response.json()]

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise GitLabAPIError(f"Request failed: {str(e)}") from e

    async def list_all_users(self) -> list[GitLabUser]:
        url: str = urljoin(self.base_url, "users")

        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response: Response = await client.get(url, headers=self._headers())

                response.raise_for_status()

                return [GitLabUser.model_validate(u) for u in response.json()]

        except HTTPStatusError as e:
            raise self._handle_http_error(e) from e

        except RequestError as e:
            raise GitLabAPIError(f"Request failed: {str(e)}") from e

    def _headers(self) -> dict[str, str]:
        return {"PRIVATE-TOKEN": self.private_token}

    @staticmethod
    def _handle_http_error(error: HTTPStatusError) -> GitLabError:
        if error.response.status_code == 401:
            return GitLabAuthenticationError()

        elif error.response.status_code == 404:
            return GitLabNotFoundError()

        else:
            return GitLabAPIError()
