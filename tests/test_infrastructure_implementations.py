import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID
from infrastructure.infrastructure_implementations import SQLAlchemySupportCaseRepository, SQLAlchemyMessageRepository
from domain.entities import SupportCase, Message
from infrastructure.models import SupportCaseModel, MessageModel

class TestSQLAlchemySupportCaseRepository(unittest.TestCase):

    def setUp(self):
        self.repo = SQLAlchemySupportCaseRepository()
        self.db_session_patch = patch('infrastructure.infrastructure_implementations.db.session')
        self.mock_db_session = self.db_session_patch.start()
        self.addCleanup(self.db_session_patch.stop)

    def test_add(self):
        case = SupportCase.create("Test Summary", "Test Description", 1)
        self.repo.add(case)
        self.mock_db_session.add.assert_called_once()
        self.mock_db_session.commit.assert_called_once()

    def test_update(self):
        case_id = UUID('12345678123456781234567812345678')
        case = SupportCase.create("Test Summary", "Test Description", 1)
        case.id = case_id
        with patch('infrastructure.infrastructure_implementations.SupportCaseModel.query.get') as mock_query:
            mock_query.return_value = SupportCaseModel(id=case_id)
            self.repo.update(case)
            self.mock_db_session.commit.assert_called_once()

    def test_delete(self):
        case_id = UUID('12345678123456781234567812345678')
        with patch('infrastructure.infrastructure_implementations.SupportCaseModel.query.get') as mock_query:
            mock_query.return_value = SupportCaseModel(id=case_id)
            self.repo.delete(case_id)
            self.mock_db_session.delete.assert_called_once()
            self.mock_db_session.commit.assert_called_once()

class TestSQLAlchemyMessageRepository(unittest.TestCase):

    def setUp(self):
        self.repo = SQLAlchemyMessageRepository()
        self.db_session_patch = patch('infrastructure.infrastructure_implementations.db.session')
        self.mock_db_session = self.db_session_patch.start()
        self.addCleanup(self.db_session_patch.stop)

    def test_add(self):
        message = Message.create(UUID('12345678123456781234567812345678'), "Test Content")
        self.repo.add(message)
        self.mock_db_session.add.assert_called_once()
        self.mock_db_session.commit.assert_called_once()

    def test_delete(self):
        message_id = UUID('87654321876543218765432187654321')
        with patch('infrastructure.infrastructure_implementations.MessageModel.query.get') as mock_query:
            mock_query.return_value = MessageModel(id=message_id)
            self.repo.delete(message_id)
            self.mock_db_session.delete.assert_called_once()
            self.mock_db_session.commit.assert_called_once()
