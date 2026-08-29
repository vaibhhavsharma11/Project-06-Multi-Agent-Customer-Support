from app.schemas.support_schemas import AgentDecision


class DemoLLMClient:
    """Deterministic LLM substitute for local development."""

    def classify_request(
        self,
        message: str,
    ) -> AgentDecision:
        """Classify a customer request deterministically."""

        if not message or not message.strip():
            raise ValueError(
                "Customer message is required."
            )

        text = message.lower()

        billing_terms = {
            "billing",
            "bill",
            "charged",
            "charge",
            "payment",
            "invoice",
            "refund",
            "subscription",
        }

        technical_terms = {
            "error",
            "bug",
            "broken",
            "crash",
            "login",
            "password",
            "technical",
            "not working",
            "failed",
        }

        if any(term in text for term in billing_terms):
            return AgentDecision(
                category="billing",
                reasoning=(
                    "The customer request concerns "
                    "billing or payment."
                ),
            )

        if any(term in text for term in technical_terms):
            return AgentDecision(
                category="technical",
                reasoning=(
                    "The customer request concerns "
                    "a technical issue."
                ),
            )

        return AgentDecision(
            category="general",
            reasoning=(
                "The customer request does not match "
                "billing or technical support."
            ),
        )