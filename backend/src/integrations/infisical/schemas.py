from pydantic import BaseModel, ConfigDict, Field


class _InfisicalBase(BaseModel):
    model_config = ConfigDict(extra="ignore")


class InfisicalEnvironment(_InfisicalBase):
    name: str
    slug: str
    id: str


class InfisicalProject(_InfisicalBase):
    id: str
    name: str
    slug: str
    description: str
    org_id: str = Field(alias="orgId")


class InfisicalIdentity(_InfisicalBase):
    client_id: str
    client_secret: str


class InfisicalProjectSetup(_InfisicalBase):
    project: InfisicalProject
    identity: InfisicalIdentity
