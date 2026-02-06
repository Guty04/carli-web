# Flujo 1. crear el proyecto -> Crear un write token -> y eso ponerlo dentro del archivo de las envs
from dataclasses import dataclass

from httpx import AsyncClient


@dataclass
class Logfire:
    logfire_url: str

    async def create_project(self, project_name: str) -> None:
        endpoint: str = f"{self.logfire_url}/"
        async with AsyncClient() as client:
            await client.post(url=endpoint)
            ...

    async def create_write_token(self, project_id: str) -> None:
        endpoint: str = f"{self.logfire_url}/"

        async with AsyncClient() as client:
            await client.post(url=endpoint)
            ...
