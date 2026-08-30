from typing import Literal

from pydantic import BaseModel, Field


SupportCategory = Literal[
    "billing",
    "technical",
    "general",
]


class SupportRequest(BaseModel):
    """Incoming customer support request."""

    message: str = Field(
        description="Customer's support message.",
    )


class AgentDecision(BaseModel):
    """Decision produced by the routing agent."""

    category: SupportCategory
    reasoning: str


class AgentResponse(BaseModel):
    """Response produced by a specialist support agent."""

    message: str
    category: SupportCategory
    resolved: bool
    escalated: bool
    escalation_reason: str | None = None
    agent: str


class SupportResponse(BaseModel):
    """Structured response produced by the support system."""

    message: str
    category: SupportCategory
    resolved: bool
    escalated: bool
    escalation_reason: str | None = None
    agent: str
    routing_reason: str
