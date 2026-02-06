from dataclasses import dataclass

from httpx import AsyncClient


@dataclass
class SonarQube:
    sonarqube_url: str

    async def create_project(self, project_name: str) -> None:
        endpoint: str = f"{self.sonarqube_url}/"
        async with AsyncClient() as client:
            await client.post(url=endpoint)
            ...

    async def get_devops_plataform(self):
        "http://localhost:9001/api/v2/dop-translation/dop-settings"
        ...
