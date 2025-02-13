"""SQLAlchemy models for persistence."""
from infrastructure.database import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class SupportCaseModel(db.Model):
    """SQLAlchemy model for support cases."""
    __tablename__ = 'support_cases'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    summary = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('MessageModel', backref='case', lazy=True, cascade='all, delete-orphan')

class MessageModel(db.Model):
    """SQLAlchemy model for messages."""
    __tablename__ = 'messages'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    case_id = db.Column(UUID(as_uuid=True), db.ForeignKey('support_cases.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)