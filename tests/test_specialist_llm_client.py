import pytest

from app.schemas.support_schemas import AgentResponse
from app.services.specialist_llm_client import (
    DemoSpecialistLLMClient,
)


def test_demo_specialist_client_handles_billing():
    client = DemoSpecialistLLMClient()

    result = client.handle_request(
        "I was charged twice.",
        "billing",
    )

    assert isinstance(result, AgentResponse)
    assert result.message
    assert result.resolved is True
    assert result.escalated is False
    assert result.escalation_reason is None


def test_demo_specialist_client_handles_technical():
    client = DemoSpecialistLLMClient()

    result = client.handle_request(
        "The application crashes.",
        "technical",
    )

    assert isinstance(result, AgentResponse)
    assert result.message
    assert result.resolved is True
    assert result.escalated is False


def test_demo_specialist_client_handles_general():
    client = DemoSpecialistLLMClient()

    result = client.handle_request(
        "Tell me more about your service.",
        "general",
    )

    assert isinstance(result, AgentResponse)
    assert result.message
    assert result.resolved is True
    assert result.escalated is False


def test_demo_specialist_client_rejects_empty_message():
    client = DemoSpecialistLLMClient()

    with pytest.raises(
        ValueError,
        match="Customer message is required.",
    ):
        client.handle_request(
            "",
            "general",
        )


def test_demo_specialist_client_is_deterministic():
    client = DemoSpecialistLLMClient()

    message = "I was charged twice."

    first = client.handle_request(
        message,
        "billing",
    )

    second = client.handle_request(
        message,
        "billing",
    )

    assert first == second