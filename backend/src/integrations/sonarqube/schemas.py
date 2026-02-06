from pydantic import BaseModel, ConfigDict


class _SonarQubeBase(BaseModel):
    model_config = ConfigDict(extra="ignore")


class SonarQubeProject(_SonarQubeBase):
    key: str
    name: str
    qualifier: str


class SonarQubeToken(_SonarQubeBase):
    name: str
    token: str
    type: str
