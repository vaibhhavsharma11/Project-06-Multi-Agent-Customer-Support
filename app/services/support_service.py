from app.agents.billing_agent import BillingAgent
from app.agents.general_agent import GeneralAgent
from app.agents.router_agent import RouterAgent
from app.agents.technical_agent import TechnicalAgent
from app.schemas.support_schemas import SupportResponse


class SupportService:
    """Orchestrate routing and specialist agents."""

    def __init__(
        self,
        router: RouterAgent,
    ) -> None:
        self.router = router
        self.agents = {
            "billing": BillingAgent(),
            "technical": TechnicalAgent(),
            "general": GeneralAgent(),
        }

    def handle_request(
        self,
        message: str,
    ) -> SupportResponse:
        """Route and handle a customer-support request."""

        message = message.strip()

        if not message:
            raise ValueError(
                "Customer message is required."
            )

        decision = self.router.route(message)

        agent = self.agents.get(
            decision.category
        )

        if agent is None:
            raise ValueError(
                f"Unsupported support category: "
                f"{decision.category}"
            )

        result = agent.handle(message)

        return SupportResponse(
            message=result.message,
            category=decision.category,
            resolved=result.resolved,
            escalated=result.escalated,
            escalation_reason=result.escalation_reason,
            agent=decision.category,
            routing_reason=decision.reasoning,
)