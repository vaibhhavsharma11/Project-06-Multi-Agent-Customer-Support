from openai import OpenAI

from app.core.llm_config import (
    get_openai_api_key,
    get_openai_model,
)
from app.schemas.support_schemas import AgentDecision


class OpenAIClientError(RuntimeError):
    """Raised when the OpenAI client cannot complete a request."""


SYSTEM_PROMPT = """
You are a customer-support routing agent.

Classify the customer's request into exactly one category:

- billing
- technical
- general

Use only the customer's supplied message.

Billing includes payments, charges, invoices, refunds,
subscriptions, and billing disputes.

Technical includes errors, bugs, crashes, login problems,
password problems, broken functionality, and technical issues.

General includes requests that do not clearly belong
to billing or technical support.

Return only the structured classification.
""".strip()


class OpenAIClient:
    """Thin wrapper around the OpenAI API."""

    def __init__(
        self,
        client: OpenAI | None = None,
        model: str | None = None,
    ) -> None:
        self.client = client or OpenAI(
            api_key=get_openai_api_key()
        )
        self.model = model or get_openai_model()

    def classify_request(
        self,
        message: str,
    ) -> AgentDecision:
        """Classify a customer request using the LLM."""

        if not message or not message.strip():
            raise OpenAIClientError(
                "Customer message is required."
            )

        try:
            response = self.client.responses.parse(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": message.strip(),
                    },
                ],
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "agent_decision",
                        "schema": AgentDecision.model_json_schema(),
                        "strict": True,
                    }
                },
            )
        except Exception as exc:
            raise OpenAIClientError(
                "OpenAI support routing request failed."
            ) from exc

        try:
            parsed = response.output_parsed
        except AttributeError as exc:
            raise OpenAIClientError(
                "OpenAI returned an unexpected response."
            ) from exc

        if parsed is None:
            raise OpenAIClientError(
                "OpenAI returned an empty routing decision."
            )

        if isinstance(parsed, AgentDecision):
            return parsed

        if hasattr(parsed, "model_dump"):
            try:
                return AgentDecision.model_validate(
                    parsed.model_dump()
                )
            except Exception as exc:
                raise OpenAIClientError(
                    "OpenAI returned an invalid routing format."
                ) from exc

        if isinstance(parsed, dict):
            try:
                return AgentDecision.model_validate(parsed)
            except Exception as exc:
                raise OpenAIClientError(
                    "OpenAI returned an invalid routing format."
                ) from exc

        raise OpenAIClientError(
            "OpenAI returned an invalid routing format."
        )