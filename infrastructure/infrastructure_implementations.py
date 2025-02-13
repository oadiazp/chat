"""SQLAlchemy implementations of repository interfaces."""
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy import desc
from infrastructure.database import db
from domain.repositories import SupportCaseRepository, MessageRepository
from domain.entities import SupportCase, Message
from infrastructure.models import SupportCaseModel, MessageModel

class SQLAlchemySupportCaseRepository(SupportCaseRepository):
    """SQLAlchemy implementation of the support case repository."""
    
    def get(self, case_id: UUID) -> Optional[SupportCase]:
        model = SupportCaseModel.query.filter_by(id=case_id).first()
        return self._to_entity(model) if model else None
    
    def get_all(self) -> List[SupportCase]:
        return [self._to_entity(model) for model in SupportCaseModel.query.all()]
    
    def add(self, case: SupportCase) -> None:
        model = self._to_model(case)
        db.session.add(model)
        db.session.commit()
    
    def update(self, case: SupportCase) -> None:
        model = SupportCaseModel.query.get(case.id)
        if model:
            model.summary = case.summary
            model.description = case.description
            model.customer_id = case.customer_id
            db.session.commit()
    
    def delete(self, case_id: UUID) -> None:
        model = SupportCaseModel.query.get(case_id)
        if model:
            db.session.delete(model)
            db.session.commit()
    
    def _to_entity(self, model: SupportCaseModel) -> SupportCase:
        return SupportCase(
            id=model.id,
            summary=model.summary,
            description=model.description,
            customer_id=model.customer_id,
            created_at=model.created_at,
            messages=[self._message_to_entity(m) for m in model.messages]
        )
    
    def _to_model(self, entity: SupportCase) -> SupportCaseModel:
        return SupportCaseModel(
            id=entity.id,
            summary=entity.summary,
            description=entity.description,
            customer_id=entity.customer_id,
            created_at=entity.created_at
        )
    
    def _message_to_entity(self, model: MessageModel) -> Message:
        return Message(
            id=model.id,
            case_id=model.case_id,
            content=model.content,
            created_at=model.created_at
        )

class SQLAlchemyMessageRepository(MessageRepository):
    """SQLAlchemy implementation of the message repository."""
    
    def get_by_case(self, case_id: UUID, limit: int = 10, offset: int = 0) -> Tuple[List[Message], int]:
        query = MessageModel.query.filter_by(case_id=case_id)
        total = query.count()
        
        models = query.order_by(desc(MessageModel.created_at))\
            .limit(limit)\
            .offset(offset)\
            .all()
            
        return [self._to_entity(model) for model in models], total
    
    def add(self, message: Message) -> None:
        model = self._to_model(message)
        db.session.add(model)
        db.session.commit()
    
    def delete(self, message_id: UUID) -> None:
        model = MessageModel.query.get(message_id)
        if model:
            db.session.delete(model)
            db.session.commit()
    
    def _to_entity(self, model: MessageModel) -> Message:
        return Message(
            id=model.id,
            case_id=model.case_id,
            content=model.content,
            created_at=model.created_at
        )
    
    def _to_model(self, entity: Message) -> MessageModel:
        return MessageModel(
            id=entity.id,
            case_id=entity.case_id,
            content=entity.content,
            created_at=entity.created_at
        )