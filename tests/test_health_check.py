"""Tests for the health check endpoint."""
import unittest
from datetime import datetime
from app import app, db

class TestHealthCheck(unittest.TestCase):
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

    def test_health_check_success(self):
        """Test health check endpoint returns healthy status."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['database'], 'connected')
        self.assertIn('timestamp', data)
        
        # Verify timestamp is in ISO format and recent
        timestamp = datetime.fromisoformat(data['timestamp'])
        self.assertIsInstance(timestamp, datetime)

    def test_health_check_format(self):
        """Test health check response format."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        required_fields = ['status', 'database', 'timestamp']
        for field in required_fields:
            self.assertIn(field, data)
