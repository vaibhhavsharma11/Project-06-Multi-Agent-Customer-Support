from app.agents.billing_agent import BillingAgent
from app.agents.general_agent import GeneralAgent
from app.agents.router_agent import RouterAgent
from app.agents.technical_agent import TechnicalAgent
from app.schemas.support_schemas import AgentDecision


class FakeRoutingClient:
    """Deterministic routing client for agent tests."""

    def classify_request(
        self,
        message: str,
    ) -> AgentDecision:
        text = message.lower()

        if "charged" in text or "subscription" in text:
            return AgentDecision(
                category="billing",
                reasoning="Billing-related request.",
            )

        if "crashes" in text or "log in" in text:
            return AgentDecision(
                category="technical",
                reasoning="Technical-support request.",
            )

        return AgentDecision(
            category="general",
            reasoning="General-support request.",
        )


def test_router_identifies_billing_request():
    router = RouterAgent(
        llm_client=FakeRoutingClient(),
    )

    decision = router.route(
        "I was charged twice for my subscription."
    )

    assert decision.category == "billing"


def test_router_identifies_technical_request():
    router = RouterAgent(
        llm_client=FakeRoutingClient(),
    )

    decision = router.route(
        "The application crashes when I try to log in."
    )

    assert decision.category == "technical"


def test_router_defaults_to_general_request():
    router = RouterAgent(
        llm_client=FakeRoutingClient(),
    )

    decision = router.route(
        "I would like to know more about your service."
    )

    assert decision.category == "general"


def test_billing_agent_returns_structured_response():
    agent = BillingAgent()

    result = agent.handle(
        "I was charged twice for my subscription."
    )

    assert result.category == "billing"
    assert result.agent == "billing"
    assert result.resolved is True
    assert result.escalated is False


def test_technical_agent_returns_structured_response():
    agent = TechnicalAgent()

    result = agent.handle(
        "The application crashes when I try to log in."
    )

    assert result.category == "technical"
    assert result.agent == "technical"
    assert result.resolved is True
    assert result.escalated is False


def test_general_agent_returns_structured_response():
    agent = GeneralAgent()

    result = agent.handle(
        "I would like to know more about your service."
    )

    assert result.category == "general"
    assert result.agent == "general"
    assert result.resolved is True
    assert result.escalated is False