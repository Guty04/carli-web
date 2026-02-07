from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class _LogfireBase(BaseModel):
    model_config = ConfigDict(extra="ignore")


class LogfireProject(_LogfireBase):
    id: UUID
    project_name: str
    created_at: datetime
    description: str | None = None
    organization_name: str
    visibility: str


class LogfireWriteToken(_LogfireBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    description: str | None = None
    token: str


class LogfireChannel(_LogfireBase):
    id: UUID
    organization_id: UUID
    label: str
    active: bool
    created_at: datetime


class LogfireAlertConfiguration(_LogfireBase):
    id: UUID
    organization_id: UUID
    project_id: UUID
    name: str
    active: bool
