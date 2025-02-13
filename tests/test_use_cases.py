import unittest
from unittest.mock import MagicMock
from uuid import UUID
from application.use_cases import SupportCaseService, MessageService
from domain.entities import SupportCase, Message

class TestSupportCaseService(unittest.TestCase):

    def setUp(self):
        self.case_repo = MagicMock()
        self.message_repo = MagicMock()
        self.service = SupportCaseService(self.case_repo, self.message_repo)

    def test_create_case(self):
        summary = "Test Summary"
        description = "Test Description"
        customer_id = 1
        case = SupportCase.create(summary, description, customer_id)
        self.case_repo.add.return_value = None

        result = self.service.create_case(summary, description, customer_id)

        self.case_repo.add.assert_called_once()
        self.assertEqual(result.summary, summary)
        self.assertEqual(result.description, description)
        self.assertEqual(result.customer_id, customer_id)

    def test_get_case(self):
        case_id = UUID('12345678123456781234567812345678')
        case = SupportCase.create("Test Summary", "Test Description", 1)
        self.case_repo.get.return_value = case

        result = self.service.get_case(case_id)

        self.case_repo.get.assert_called_once_with(case_id)
        self.assertEqual(result, case)

    def test_get_all_cases(self):
        cases = [SupportCase.create("Test Summary", "Test Description", 1)]
        self.case_repo.get_all.return_value = cases

        result = self.service.get_all_cases()

        self.case_repo.get_all.assert_called_once()
        self.assertEqual(result, cases)

    def test_update_case(self):
        case_id = UUID('12345678123456781234567812345678')
        case = SupportCase.create("Old Summary", "Old Description", 1)
        self.case_repo.get.return_value = case

        result = self.service.update_case(case_id, "New Summary", "New Description", 2)

        self.case_repo.update.assert_called_once_with(case)
        self.assertEqual(result.summary, "New Summary")
        self.assertEqual(result.description, "New Description")
        self.assertEqual(result.customer_id, 2)

    def test_delete_case(self):
        case_id = UUID('12345678123456781234567812345678')
        case = SupportCase.create("Test Summary", "Test Description", 1)
        self.case_repo.get.return_value = case

        result = self.service.delete_case(case_id)

        self.case_repo.delete.assert_called_once_with(case_id)
        self.assertTrue(result)

class TestMessageService(unittest.TestCase):

    def setUp(self):
        self.case_repo = MagicMock()
        self.message_repo = MagicMock()
        self.service = MessageService(self.case_repo, self.message_repo)

    def test_add_message(self):
        case_id = UUID('12345678123456781234567812345678')
        content = "Test Message Content"
        case = SupportCase.create("Test Summary", "Test Description", 1)
        self.case_repo.get.return_value = case
        message = case.add_message(content)
        self.message_repo.add.return_value = None

        result = self.service.add_message(case_id, content)

        self.message_repo.add.assert_called_once()
        self.assertEqual(result.content, content)

    def test_get_case_messages(self):
        case_id = UUID('12345678123456781234567812345678')
        messages = [Message.create(case_id, "Test Message Content")]
        self.case_repo.get.return_value = SupportCase.create("Test Summary", "Test Description", 1)
        self.message_repo.get_by_case.return_value = (messages, 1)

        result, total = self.service.get_case_messages(case_id)

        self.message_repo.get_by_case.assert_called_once_with(case_id, 10, 0)
        self.assertEqual(result, messages)
        self.assertEqual(total, 1)

    def test_delete_message(self):
        case_id = UUID('12345678123456781234567812345678')
        message_id = UUID('87654321876543218765432187654321')

        result = self.service.delete_message(case_id, message_id)

        self.message_repo.delete.assert_called_once_with(message_id)
        self.assertTrue(result)
