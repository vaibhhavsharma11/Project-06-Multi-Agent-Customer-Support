from typing import Protocol

from app.schemas.support_schemas import AgentDecision


class RoutingClient(Protocol):
    """Interface required by the router."""

    def classify_request(
        self,
        message: str,
    ) -> AgentDecision:
        ...


class RouterAgent:
    """Route customer requests using an AI classification client."""

    def __init__(
        self,
        llm_client: RoutingClient,
    ) -> None:
        self.llm_client = llm_client

    def route(
        self,
        message: str,
    ) -> AgentDecision:
        """Classify a customer request."""

        if not message or not message.strip():
            raise ValueError(
                "Customer message is required."
            )

        return self.llm_client.classify_request(
            message.strip()
        )