"""Repository interfaces for the domain."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .entities import SupportCase, Message

class SupportCaseRepository(ABC):
    """Interface for support case persistence."""
    
    @abstractmethod
    def get(self, case_id: UUID) -> Optional[SupportCase]:
        """Retrieve a support case by ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[SupportCase]:
        """Retrieve all support cases."""
        pass
    
    @abstractmethod
    def add(self, case: SupportCase) -> None:
        """Add a new support case."""
        pass
    
    @abstractmethod
    def update(self, case: SupportCase) -> None:
        """Update an existing support case."""
        pass
    
    @abstractmethod
    def delete(self, case_id: UUID) -> None:
        """Delete a support case."""
        pass

class MessageRepository(ABC):
    """Interface for message persistence."""
    
    @abstractmethod
    def get_by_case(self, case_id: UUID, limit: int = 10, offset: int = 0) -> tuple[List[Message], int]:
        """Retrieve messages for a case with pagination."""
        pass
    
    @abstractmethod
    def add(self, message: Message) -> None:
        """Add a new message."""
        pass
    
    @abstractmethod
    def delete(self, message_id: UUID) -> None:
        """Delete a message."""
        pass
