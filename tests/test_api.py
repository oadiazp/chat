import unittest
import json
from app import app, db
import uuid
from infrastructure.models import SupportCaseModel, MessageModel
from domain.entities import SupportCase, Message
from infrastructure.infrastructure_implementations import SQLAlchemySupportCaseRepository, SQLAlchemyMessageRepository
from application.use_cases import SupportCaseService, MessageService

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        # Initialize repositories and services for testing
        cls.case_repository = SQLAlchemySupportCaseRepository()
        cls.message_repository = SQLAlchemyMessageRepository()
        cls.case_service = SupportCaseService(cls.case_repository, cls.message_repository)
        cls.message_service = MessageService(cls.case_repository, cls.message_repository)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        # Clear any existing data
        db.session.query(MessageModel).delete()
        db.session.query(SupportCaseModel).delete()
        db.session.commit()

    def tearDown(self):
        # Clear data between tests
        db.session.query(MessageModel).delete()
        db.session.query(SupportCaseModel).delete()
        db.session.commit()

    def create_test_case(self):
        """Helper method to create a test support case"""
        data = {
            "summary": "Test Support Case",
            "description": "This is a test support case",
            "customer_id": 1
        }
        response = self.client.post('/api/cases',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)

        json_data = json.loads(response.data)
        self.assertIn('id', json_data)
        self.assertEqual(json_data['summary'], data['summary'])
        self.assertEqual(json_data['description'], data['description'])
        self.assertEqual(json_data['customer_id'], data['customer_id'])

        return json_data['id']

    def test_create_support_case(self):
        """Test creating a new support case"""
        self.create_test_case()  # Just verify creation works

    def test_get_support_case(self):
        """Test retrieving a support case"""
        case_id = self.create_test_case()
        response = self.client.get(f'/api/cases/{case_id}')
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        self.assertEqual(json_data['id'], case_id)

    def test_create_and_get_message(self):
        """Test creating and retrieving a message for a support case"""
        case_id = self.create_test_case()

        # Create message
        message_data = {
            "content": "This is a test message"
        }
        response = self.client.post(f'/api/cases/{case_id}/messages',
                                data=json.dumps(message_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)

        json_data = json.loads(response.data)
        self.assertIn('id', json_data)
        self.assertEqual(json_data['content'], message_data['content'])

        # Get messages for the case
        response = self.client.get(f'/api/cases/{case_id}/messages')
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        self.assertIn('messages', json_data)
        self.assertIn('pagination', json_data)
        self.assertEqual(len(json_data['messages']), 1)
        self.assertEqual(json_data['messages'][0]['content'], message_data['content'])
        self.assertEqual(json_data['pagination']['total'], 1)

    def test_message_pagination(self):
        """Test paginated message retrieval"""
        case_id = self.create_test_case()

        # Create 15 messages
        for i in range(15):
            message_data = {
                "content": f"Test message {i}"
            }
            response = self.client.post(f'/api/cases/{case_id}/messages',
                                    data=json.dumps(message_data),
                                    content_type='application/json')
            self.assertEqual(response.status_code, 201)

        # Test default pagination (limit=10, offset=0)
        response = self.client.get(f'/api/cases/{case_id}/messages')
        json_data = json.loads(response.data)
        self.assertEqual(len(json_data['messages']), 10)
        self.assertEqual(json_data['pagination']['total'], 15)
        self.assertEqual(json_data['pagination']['limit'], 10)
        self.assertEqual(json_data['pagination']['offset'], 0)

        # Test custom pagination
        response = self.client.get(f'/api/cases/{case_id}/messages?limit=5&offset=10')
        json_data = json.loads(response.data)
        self.assertEqual(len(json_data['messages']), 5)
        self.assertEqual(json_data['pagination']['total'], 15)
        self.assertEqual(json_data['pagination']['limit'], 5)
        self.assertEqual(json_data['pagination']['offset'], 10)
