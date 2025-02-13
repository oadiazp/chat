import unittest
import uuid
from app import app, db
from infrastructure.models import SupportCaseModel, MessageModel
from datetime import datetime, timedelta

class TestMessageResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.client = app.test_client()

        # Create a test case using the model directly (for test setup only)
        self.test_case = SupportCaseModel(
            summary="Test Case",
            description="Test Description",
            customer_id=1
        )
        db.session.add(self.test_case)
        db.session.commit()

        # Store the case_id for later use
        self.case_id = str(self.test_case.id)

        # Create test messages
        base_time = datetime.utcnow()
        for i in range(15):  # Create 15 messages
            message = MessageModel(
                case_id=self.test_case.id,
                content=f"Test message {i}",
                created_at=base_time - timedelta(minutes=i)  # Messages spaced 1 minute apart
            )
            db.session.add(message)
        db.session.commit()

    def tearDown(self):
        # Clear data between tests
        db.session.query(MessageModel).delete()
        db.session.query(SupportCaseModel).delete()
        db.session.commit()

    def test_get_messages_pagination(self):
        """Test that messages are correctly paginated"""
        # Test default pagination (limit=10, offset=0)
        response = self.client.get(f'/api/cases/{self.case_id}/messages')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['messages']), 10)
        self.assertEqual(data['pagination']['total'], 15)
        self.assertEqual(data['pagination']['offset'], 0)
        self.assertEqual(data['pagination']['limit'], 10)

        # Test custom limit and offset
        response = self.client.get(
            f'/api/cases/{self.case_id}/messages?limit=5&offset=10'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['messages']), 5)
        self.assertEqual(data['pagination']['offset'], 10)
        self.assertEqual(data['pagination']['limit'], 5)

    def test_get_messages_ordering(self):
        """Test that messages are returned in descending order by created_at"""
        response = self.client.get(f'/api/cases/{self.case_id}/messages')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Check that messages are in descending order
        messages = data['messages']
        for i in range(len(messages) - 1):
            current = datetime.fromisoformat(messages[i]['created_at'])
            next_msg = datetime.fromisoformat(messages[i + 1]['created_at'])
            self.assertGreater(current, next_msg)

    def test_get_messages_invalid_case(self):
        """Test that requesting messages for non-existent case returns 404"""
        random_uuid = str(uuid.uuid4())
        response = self.client.get(f'/api/cases/{random_uuid}/messages')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Support case not found"})

    def test_get_messages_invalid_parameters(self):
        """Test that invalid pagination parameters return 400"""
        # Test invalid limit
        response = self.client.get(
            f'/api/cases/{self.case_id}/messages?limit=invalid'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Invalid pagination parameters"}
        )

        # Test invalid offset
        response = self.client.get(
            f'/api/cases/{self.case_id}/messages?offset=invalid'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Invalid pagination parameters"}
        )
