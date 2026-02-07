from typing import Any

from pydantic import BaseModel, ConfigDict


class LogfireAlert(BaseModel):
    model_config = ConfigDict(extra="ignore")

    project_id: str
    trace_id: str
    message: str
    request: dict[str, Any]
    exception_message: str
    stack_trace: str
