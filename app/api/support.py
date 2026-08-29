from fastapi import APIRouter, HTTPException

from app.agents.router_agent import RouterAgent
from app.core.llm_config import is_demo_mode
from app.schemas.support_schemas import (
    SupportRequest,
    SupportResponse,
)
from app.services.demo_llm_client import DemoLLMClient
from app.services.openai_client import OpenAIClient
from app.services.support_service import SupportService


router = APIRouter(
    prefix="/support",
    tags=["support"],
)


def _build_support_service() -> SupportService:
    """Build the customer-support service with its routing client."""

    if is_demo_mode():
        llm_client = DemoLLMClient()
    else:
        llm_client = OpenAIClient()

    router_agent = RouterAgent(
        llm_client=llm_client,
    )

    return SupportService(
        router=router_agent,
    )


@router.get("/health")
def support_health_check():
    """Return the health status of the support service."""

    return {
        "status": "healthy",
        "service": "customer-support",
    }


@router.post(
    "/handle",
    response_model=SupportResponse,
)
def handle_support_request(
    request: SupportRequest,
):
    """Route and handle a customer-support request."""

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Customer message is required.",
        )

    try:
        service = _build_support_service()

        return service.handle_request(
            message,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Customer support request failed.",
        ) from exc