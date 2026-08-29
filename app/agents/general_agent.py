from app.schemas.support_schemas import (
    AgentResponse,
)
from app.services.specialist_llm_client import (
    DemoSpecialistLLMClient,
    SpecialistLLMClient,
)


class GeneralAgent:
    """Handle general customer requests."""

    def __init__(
        self,
        llm_client: SpecialistLLMClient | None = None,
    ) -> None:
        self.llm_client = (
            llm_client
            or DemoSpecialistLLMClient()
        )

    def handle(
        self,
        message: str,
    ) -> AgentResponse:
        """Handle a general request."""

        return self.llm_client.handle_request(
            message,
            "general",
        )