from abc import ABC, abstractmethod

from app.schemas.support_schemas import SupportResponse


class BaseSupportAgent(ABC):
    """Base interface for customer-support specialist agents."""

    name: str

    @abstractmethod
    def handle(self, message: str) -> SupportResponse:
        """Handle a customer-support request."""
        raise NotImplementedError