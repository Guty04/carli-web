from pydantic import BaseModel, ConfigDict, Field


class _JiraBase(BaseModel):
    model_config = ConfigDict(extra="ignore")


class JiraIssue(_JiraBase):
    id: str
    key: str
    self_url: str = Field(alias="self")
