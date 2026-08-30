from app.agents.router_agent import RouterAgent
from app.schemas.support_schemas import AgentDecision, AgentResponse
from app.services.support_service import SupportService


class StubRoutingClient:
    def __init__(self, decision: AgentDecision):
        self.decision = decision
        self.received_message = None

    def classify_request(
        self,
        message: str,
    ) -> AgentDecision:
        self.received_message = message
        return self.decision


class StubSpecialistClient:
    def __init__(self, response: AgentResponse):
        self.response = response
        self.received_message = None
        self.received_category = None

    def handle_request(
        self,
        message: str,
        category: str,
    ) -> AgentResponse:
        self.received_message = message
        self.received_category = category
        return self.response


def test_support_service_routes_billing_request_to_billing_agent():
    routing_client = StubRoutingClient(
        AgentDecision(
            category="billing",
            reasoning="The customer is asking about an invoice.",
        )
    )

    service = SupportService(
        router=RouterAgent(routing_client),
    )

    specialist_client = StubSpecialistClient(
        AgentResponse(
            message="Your invoice has been reviewed.",
            category="billing",
            resolved=True,
            escalated=False,
            escalation_reason=None,
            agent="billing",
        )
    )

    service.agents["billing"].llm_client = specialist_client

    result = service.handle_request(
        "  I have a question about my invoice.  "
    )

    assert result.category == "billing"
    assert result.agent == "billing"
    assert result.message == "Your invoice has been reviewed."
    assert result.resolved is True
    assert result.escalated is False
    assert (
        result.routing_reason
        == "The customer is asking about an invoice."
    )

    assert (
        routing_client.received_message
        == "I have a question about my invoice."
    )

    assert (
        specialist_client.received_message
        == "I have a question about my invoice."
    )
    assert specialist_client.received_category == "billing"


def test_support_service_routes_technical_request_to_technical_agent():
    routing_client = StubRoutingClient(
        AgentDecision(
            category="technical",
            reasoning="The customer is reporting a technical problem.",
        )
    )

    service = SupportService(
        router=RouterAgent(routing_client),
    )

    specialist_client = StubSpecialistClient(
        AgentResponse(
            message="Please restart the application and try again.",
            category="technical",
            resolved=False,
            escalated=True,
            escalation_reason="Issue requires technical investigation.",
            agent="technical",
        )
    )

    service.agents["technical"].llm_client = specialist_client

    result = service.handle_request(
        "The application keeps crashing."
    )

    assert result.category == "technical"
    assert result.agent == "technical"
    assert result.escalated is True
    assert (
        result.escalation_reason
        == "Issue requires technical investigation."
    )
    assert (
        result.routing_reason
        == "The customer is reporting a technical problem."
    )
    assert specialist_client.received_category == "technical"


def test_support_service_routes_general_request_to_general_agent():
    routing_client = StubRoutingClient(
        AgentDecision(
            category="general",
            reasoning="The request does not match a specialist category.",
        )
    )

    service = SupportService(
        router=RouterAgent(routing_client),
    )

    specialist_client = StubSpecialistClient(
        AgentResponse(
            message="Here is some general information.",
            category="general",
            resolved=True,
            escalated=False,
            escalation_reason=None,
            agent="general",
        )
    )

    service.agents["general"].llm_client = specialist_client

    result = service.handle_request(
        "Can you tell me more about your service?"
    )

    assert result.category == "general"
    assert result.agent == "general"
    assert result.resolved is True
    assert result.escalated is False
    assert (
        result.routing_reason
        == "The request does not match a specialist category."
    )
    assert specialist_client.received_category == "general"


def test_support_service_rejects_empty_message():
    routing_client = StubRoutingClient(
        AgentDecision(
            category="general",
            reasoning="General request.",
        )
    )

    service = SupportService(
        router=RouterAgent(routing_client),
    )

    try:
        service.handle_request("   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Customer message is required."
