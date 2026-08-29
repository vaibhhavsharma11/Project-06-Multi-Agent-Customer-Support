from unittest.mock import Mock

import pytest

from app.schemas.support_schemas import AgentDecision
from app.services.demo_llm_client import DemoLLMClient
from app.services.openai_client import (
    OpenAIClient,
    OpenAIClientError,
)


def test_demo_llm_client_returns_billing_decision():
    client = DemoLLMClient()

    result = client.classify_request(
        "I was charged twice for my subscription."
    )

    assert isinstance(result, AgentDecision)
    assert result.category == "billing"


def test_demo_llm_client_returns_technical_decision():
    client = DemoLLMClient()

    result = client.classify_request(
        "The application crashes when I try to log in."
    )

    assert isinstance(result, AgentDecision)
    assert result.category == "technical"


def test_demo_llm_client_returns_general_decision():
    client = DemoLLMClient()

    result = client.classify_request(
        "I would like to learn more about your service."
    )

    assert isinstance(result, AgentDecision)
    assert result.category == "general"


def test_demo_llm_client_rejects_empty_message():
    client = DemoLLMClient()

    with pytest.raises(
        ValueError,
        match="Customer message is required.",
    ):
        client.classify_request("")


def test_demo_llm_client_is_deterministic():
    client = DemoLLMClient()

    message = "I was charged twice for my subscription."

    first = client.classify_request(message)
    second = client.classify_request(message)

    assert first == second


def test_openai_client_uses_configured_model():
    mock_client = Mock()

    mock_response = Mock()
    mock_response.output_parsed = AgentDecision(
        category="billing",
        reasoning="Billing request.",
    )

    mock_client.responses.parse.return_value = mock_response

    client = OpenAIClient(
        client=mock_client,
        model="test-model",
    )

    result = client.classify_request(
        "I was charged twice."
    )

    assert result.category == "billing"

    mock_client.responses.parse.assert_called_once()

    call_kwargs = (
        mock_client.responses.parse.call_args.kwargs
    )

    assert call_kwargs["model"] == "test-model"


def test_openai_client_sends_customer_message():
    mock_client = Mock()

    mock_response = Mock()
    mock_response.output_parsed = AgentDecision(
        category="technical",
        reasoning="Technical request.",
    )

    mock_client.responses.parse.return_value = mock_response

    client = OpenAIClient(
        client=mock_client,
        model="test-model",
    )

    message = "The application is not working."

    result = client.classify_request(message)

    assert result.category == "technical"

    call_kwargs = (
        mock_client.responses.parse.call_args.kwargs
    )

    assert message in str(call_kwargs["input"])


def test_openai_client_strips_message():
    mock_client = Mock()

    mock_response = Mock()
    mock_response.output_parsed = AgentDecision(
        category="general",
        reasoning="General request.",
    )

    mock_client.responses.parse.return_value = mock_response

    client = OpenAIClient(
        client=mock_client,
        model="test-model",
    )

    client.classify_request(
        "   Tell me more about the service.   "
    )

    call_kwargs = (
        mock_client.responses.parse.call_args.kwargs
    )

    assert (
        "Tell me more about the service."
        in str(call_kwargs["input"])
    )


def test_openai_client_rejects_empty_message():
    mock_client = Mock()

    client = OpenAIClient(
        client=mock_client,
        model="test-model",
    )

    with pytest.raises(
        OpenAIClientError,
        match="Customer message is required.",
    ):
        client.classify_request("")


def test_openai_client_wraps_api_failure():
    mock_client = Mock()

    mock_client.responses.parse.side_effect = RuntimeError(
        "API unavailable"
    )

    client = OpenAIClient(
        client=mock_client,
        model="test-model",
    )

    with pytest.raises(
        OpenAIClientError,
        match="OpenAI support routing request failed.",
    ):
        client.classify_request(
            "I need help with my account."
        )


def test_openai_client_rejects_empty_response():
    mock_client = Mock()

    mock_response = Mock()
    mock_response.output_parsed = None

    mock_client.responses.parse.return_value = mock_response

    client = OpenAIClient(
        client=mock_client,
        model="test-model",
    )

    with pytest.raises(
        OpenAIClientError,
        match="OpenAI returned an empty routing decision.",
    ):
        client.classify_request(
            "I need help with my account."
        )


def test_openai_client_validates_dict_response():
    mock_client = Mock()

    mock_response = Mock()
    mock_response.output_parsed = {
        "category": "general",
        "reasoning": "General request.",
    }

    mock_client.responses.parse.return_value = mock_response

    client = OpenAIClient(
        client=mock_client,
        model="test-model",
    )

    result = client.classify_request(
        "Tell me more about the service."
    )

    assert isinstance(result, AgentDecision)
    assert result.category == "general"


def test_openai_client_rejects_invalid_response():
    mock_client = Mock()

    mock_response = Mock()
    mock_response.output_parsed = {
        "category": "unsupported",
        "reasoning": "Invalid category.",
    }

    mock_client.responses.parse.return_value = mock_response

    client = OpenAIClient(
        client=mock_client,
        model="test-model",
    )

    with pytest.raises(
        OpenAIClientError,
        match="OpenAI returned an invalid routing format.",
    ):
        client.classify_request(
            "I need help with something."
        )