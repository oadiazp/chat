import unittest
from uuid import UUID
from domain.entities import SupportCase, Message

class TestSupportCase(unittest.TestCase):

    def test_create_support_case(self):
        """Test the creation of a support case."""
        summary = "Test Summary"
        description = "Test Description"
        customer_id = 1

        support_case = SupportCase.create(summary, description, customer_id)

        self.assertIsInstance(support_case.id, UUID)
        self.assertEqual(support_case.summary, summary)
        self.assertEqual(support_case.description, description)
        self.assertEqual(support_case.customer_id, customer_id)
        self.assertEqual(len(support_case.messages), 0)

    def test_add_message(self):
        """Test adding a message to a support case."""
        summary = "Test Summary"
        description = "Test Description"
        customer_id = 1

        support_case = SupportCase.create(summary, description, customer_id)
        content = "Test Message Content"

        message = support_case.add_message(content)

        self.assertIsInstance(message.id, UUID)
        self.assertEqual(message.case_id, support_case.id)
        self.assertEqual(message.content, content)
        self.assertEqual(len(support_case.messages), 1)
        self.assertEqual(support_case.messages[0], message)


import unittest
from uuid import UUID
from domain.entities import Message

class TestMessage(unittest.TestCase):

    def test_create_message(self):
        """Test the creation of a message."""
        case_id = UUID('12345678123456781234567812345678')
        content = "Test Message Content"

        message = Message.create(case_id, content)

        self.assertIsInstance(message.id, UUID)
        self.assertEqual(message.case_id, case_id)
        self.assertEqual(message.content, content)
        self.assertIsNotNone(message.created_at)
