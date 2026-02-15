from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LogfireAlert(BaseModel):
    model_config = ConfigDict(extra="ignore")

    project_id: UUID
    trace_id: str
    message: str
    request: dict[str, str | int | float | bool]
    exception_message: str
    stack_trace: str
