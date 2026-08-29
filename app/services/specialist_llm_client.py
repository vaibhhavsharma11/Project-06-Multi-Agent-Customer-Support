from typing import Protocol

from app.schemas.support_schemas import (
    AgentResponse,
    SupportCategory,
)


class SpecialistLLMClient(Protocol):
    """Interface for specialist support LLM clients."""

    def handle_request(
        self,
        message: str,
        category: SupportCategory,
    ) -> AgentResponse:
        ...


class DemoSpecialistLLMClient:
    """Deterministic specialist LLM substitute."""

    def handle_request(
        self,
        message: str,
        category: SupportCategory,
    ) -> AgentResponse:
        """Return a deterministic specialist response."""

        if not message or not message.strip():
            raise ValueError(
                "Customer message is required."
            )

        message = message.strip()

        if category == "billing":
            return AgentResponse(
                message=(
                    "I can help review the billing issue. "
                    "Please check your billing history for "
                    "the duplicate charge. If the duplicate "
                    "charge remains, our billing team can "
                    "investigate the transaction."
                ),
                category="billing",
                resolved=True,
                escalated=False,
                escalation_reason=None,
                agent="billing",
            )

        if category == "technical":
            return AgentResponse(
                message=(
                    "Please try signing out and back in, "
                    "then retry the action. If the problem "
                    "continues, our technical team can "
                    "investigate the issue further."
                ),
                category="technical",
                resolved=True,
                escalated=False,
                escalation_reason=None,
                agent="technical",
            )

        return AgentResponse(
            message=(
                "I'd be happy to help. Please provide "
                "a little more detail about what you need "
                "assistance with."
            ),
            category="general",
            resolved=True,
            escalated=False,
            escalation_reason=None,
            agent="general",
        )