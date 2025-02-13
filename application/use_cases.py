"""Application use cases implementing the business logic."""
from typing import List, Optional, Tuple
from uuid import UUID
from domain.entities import SupportCase, Message
from domain.repositories import SupportCaseRepository, MessageRepository

class SupportCaseService:
    """Application service for managing support cases."""
    
    def __init__(self, case_repo: SupportCaseRepository, message_repo: MessageRepository):
        self.case_repo = case_repo
        self.message_repo = message_repo
    
    def create_case(self, summary: str, description: str, customer_id: int) -> SupportCase:
        """Create a new support case."""
        case = SupportCase.create(summary, description, customer_id)
        self.case_repo.add(case)
        return case
    
    def get_case(self, case_id: UUID) -> Optional[SupportCase]:
        """Get a support case by ID."""
        return self.case_repo.get(case_id)
    
    def get_all_cases(self) -> List[SupportCase]:
        """Get all support cases."""
        return self.case_repo.get_all()
    
    def update_case(self, case_id: UUID, summary: str, description: str, customer_id: int) -> Optional[SupportCase]:
        """Update an existing support case."""
        case = self.case_repo.get(case_id)
        if not case:
            return None
            
        case.summary = summary
        case.description = description
        case.customer_id = customer_id
        self.case_repo.update(case)
        return case
    
    def delete_case(self, case_id: UUID) -> bool:
        """Delete a support case."""
        case = self.case_repo.get(case_id)
        if not case:
            return False
        self.case_repo.delete(case_id)
        return True

class MessageService:
    """Application service for managing messages."""
    
    def __init__(self, case_repo: SupportCaseRepository, message_repo: MessageRepository):
        self.case_repo = case_repo
        self.message_repo = message_repo
    
    def add_message(self, case_id: UUID, content: str) -> Optional[Message]:
        """Add a new message to a support case."""
        case = self.case_repo.get(case_id)
        if not case:
            return None
            
        message = case.add_message(content)
        self.message_repo.add(message)
        return message
    
    def get_case_messages(self, case_id: UUID, limit: int = 10, offset: int = 0) -> Tuple[List[Message], int]:
        """Get messages for a case with pagination."""
        case = self.case_repo.get(case_id)
        if not case:
            return [], 0
            
        return self.message_repo.get_by_case(case_id, limit, offset)
    
    def delete_message(self, case_id: UUID, message_id: UUID) -> bool:
        """Delete a message from a support case."""
        self.message_repo.delete(message_id)
        return True
