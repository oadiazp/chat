"""Domain entities for the support ticket system."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

@dataclass
class SupportCase:
    """Support case entity representing a customer support ticket."""
    id: UUID
    summary: str
    description: str
    customer_id: int
    created_at: datetime
    messages: List['Message']

    @classmethod
    def create(cls, summary: str, description: str, customer_id: int) -> 'SupportCase':
        """Factory method to create a new support case."""
        return cls(
            id=uuid4(),
            summary=summary,
            description=description,
            customer_id=customer_id,
            created_at=datetime.utcnow(),
            messages=[]
        )

    def add_message(self, content: str) -> 'Message':
        """Add a new message to this support case."""
        message = Message.create(self.id, content)
        self.messages.append(message)
        return message

@dataclass
class Message:
    """Message entity representing a communication in a support case."""
    id: UUID
    case_id: UUID
    content: str
    created_at: datetime

    @classmethod
    def create(cls, case_id: UUID, content: str) -> 'Message':
        """Factory method to create a new message."""
        return cls(
            id=uuid4(),
            case_id=case_id,
            content=content,
            created_at=datetime.utcnow()
        )
