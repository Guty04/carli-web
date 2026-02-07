import json
from dataclasses import dataclass, field
from pathlib import Path

from pydantic_ai import Agent, AgentRunResult
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from src.errors.gemini import GeminiAPIError
from src.schemas.webhook import LogfireAlert

from .schemas import JiraTicketContent

_PROMPT_FILE: Path = Path(__file__).parent / "SYSTEM_PROMPT.md"
SYSTEM_PROMPT: str = _PROMPT_FILE.read_text()


@dataclass
class TicketAgent:
    api_key: str
    model_name: str
    _agent: Agent[None, JiraTicketContent] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        provider = GoogleProvider(api_key=self.api_key)
        model = GoogleModel(self.model_name, provider=provider)
        self._agent = Agent(
            model=model,
            output_type=JiraTicketContent,
            system_prompt=SYSTEM_PROMPT,
        )

    async def analyze_alert(self, alert: LogfireAlert) -> JiraTicketContent:
        prompt = (
            f"Exception Message: {alert.exception_message}\n\n"
            f"Log Message: {alert.message}\n\n"
            f"Stack Trace:\n{alert.stack_trace}\n\n"
            f"Request Context:\n{json.dumps(alert.request, indent=2)}"
        )

        try:
            result: AgentRunResult[JiraTicketContent] = await self._agent.run(prompt)
            return result.output
        except Exception as e:
            raise GeminiAPIError(f"Agent failed to analyze alert: {e!s}") from e
