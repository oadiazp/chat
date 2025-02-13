"""Flask routes implementation."""
from flask import request
from flask_restful import Resource
from uuid import UUID
import logging
from datetime import datetime
from application.use_cases import SupportCaseService, MessageService
from infrastructure.infrastructure_implementations import SQLAlchemySupportCaseRepository, SQLAlchemyMessageRepository
from validators import validate_support_case, validate_message

logger = logging.getLogger(__name__)

# Initialize repositories and services
case_repository = SQLAlchemySupportCaseRepository()
message_repository = SQLAlchemyMessageRepository()
case_service = SupportCaseService(case_repository, message_repository)
message_service = MessageService(case_repository, message_repository)

class HealthCheckResource(Resource):
    """REST resource for health check."""

    def get(self):
        """Return health status of the application."""
        try:
            # Check database connection by making a simple query
            case_repository.get_all()
            return {
                "status": "healthy",
                "database": "connected",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }, 503

class SupportCaseResource(Resource):
    """REST resource for support cases."""

    def get(self, case_id=None):
        try:
            if case_id:
                try:
                    uuid_obj = UUID(case_id)
                except ValueError:
                    return {"error": "Invalid UUID format"}, 400

                case = case_service.get_case(uuid_obj)
                if not case:
                    return {"error": "Support case not found"}, 404

                return {
                    'id': str(case.id),
                    'summary': case.summary,
                    'description': case.description,
                    'customer_id': case.customer_id,
                    'created_at': case.created_at.isoformat()
                }

            cases = case_service.get_all_cases()
            return [{
                'id': str(case.id),
                'summary': case.summary,
                'description': case.description,
                'customer_id': case.customer_id,
                'created_at': case.created_at.isoformat()
            } for case in cases]

        except Exception as e:
            logger.error(f"Error retrieving support case: {str(e)}")
            return {"error": "Internal server error"}, 500

    def post(self):
        try:
            data = request.get_json()
            if not validate_support_case(data):
                return {"error": "Invalid support case data"}, 400

            case = case_service.create_case(
                summary=data["summary"],
                description=data["description"],
                customer_id=data["customer_id"]
            )

            return {
                'id': str(case.id),
                'summary': case.summary,
                'description': case.description,
                'customer_id': case.customer_id,
                'created_at': case.created_at.isoformat()
            }, 201

        except Exception as e:
            logger.error(f"Error creating support case: {str(e)}")
            return {"error": "Internal server error"}, 500

    def put(self, case_id):
        try:
            try:
                uuid_obj = UUID(case_id)
            except ValueError:
                return {"error": "Invalid UUID format"}, 400

            data = request.get_json()
            if not validate_support_case(data):
                return {"error": "Invalid support case data"}, 400

            case = case_service.update_case(
                case_id=uuid_obj,
                summary=data["summary"],
                description=data["description"],
                customer_id=data["customer_id"]
            )

            if not case:
                return {"error": "Support case not found"}, 404

            return {
                'id': str(case.id),
                'summary': case.summary,
                'description': case.description,
                'customer_id': case.customer_id,
                'created_at': case.created_at.isoformat()
            }

        except Exception as e:
            logger.error(f"Error updating support case: {str(e)}")
            return {"error": "Internal server error"}, 500

    def delete(self, case_id):
        try:
            try:
                uuid_obj = UUID(case_id)
            except ValueError:
                return {"error": "Invalid UUID format"}, 400

            if case_service.delete_case(uuid_obj):
                return "", 204
            return {"error": "Support case not found"}, 404

        except Exception as e:
            logger.error(f"Error deleting support case: {str(e)}")
            return {"error": "Internal server error"}, 500

class MessageResource(Resource):
    """REST resource for messages."""

    def get(self, case_id):
        try:
            try:
                uuid_obj = UUID(case_id)
            except ValueError:
                return {"error": "Invalid UUID format"}, 400

            # Check if case exists first
            case = case_service.get_case(uuid_obj)
            if not case:
                return {"error": "Support case not found"}, 404

            try:
                limit = min(int(request.args.get('limit', 10)), 100)
                offset = max(int(request.args.get('offset', 0)), 0)
            except ValueError:
                return {"error": "Invalid pagination parameters"}, 400

            messages, total = message_service.get_case_messages(uuid_obj, limit, offset)
            return {
                "messages": [{
                    'id': str(message.id),
                    'case_id': str(message.case_id),
                    'content': message.content,
                    'created_at': message.created_at.isoformat()
                } for message in messages],
                "pagination": {
                    "total": total,
                    "offset": offset,
                    "limit": limit
                }
            }

        except Exception as e:
            logger.error(f"Error retrieving messages: {str(e)}")
            return {"error": "Internal server error"}, 500

    def post(self, case_id):
        try:
            try:
                uuid_obj = UUID(case_id)
            except ValueError:
                return {"error": "Invalid UUID format"}, 400

            # Check if case exists first
            case = case_service.get_case(uuid_obj)
            if not case:
                return {"error": "Support case not found"}, 404

            data = request.get_json()
            if not validate_message(data):
                return {"error": "Invalid message data"}, 400

            message = message_service.add_message(uuid_obj, data["content"])
            if not message:
                return {"error": "Failed to create message"}, 500

            return {
                'id': str(message.id),
                'case_id': str(message.case_id),
                'content': message.content,
                'created_at': message.created_at.isoformat()
            }, 201

        except Exception as e:
            logger.error(f"Error creating message: {str(e)}")
            return {"error": "Internal server error"}, 500

    def delete(self, case_id, message_id):
        try:
            try:
                case_uuid = UUID(case_id)
                message_uuid = UUID(message_id)
            except ValueError:
                return {"error": "Invalid UUID format"}, 400

            # Check if case exists first
            case = case_service.get_case(case_uuid)
            if not case:
                return {"error": "Support case not found"}, 404

            if message_service.delete_message(case_uuid, message_uuid):
                return "", 204
            return {"error": "Message not found"}, 404

        except Exception as e:
            logger.error(f"Error deleting message: {str(e)}")
            return {"error": "Internal server error"}, 500

def initialize_routes(api):
    """Initialize the API routes."""
    api.add_resource(HealthCheckResource, '/health')
    api.add_resource(SupportCaseResource, 
                    '/api/cases',
                    '/api/cases/<string:case_id>')
    api.add_resource(MessageResource,
                    '/api/cases/<string:case_id>/messages',
                    '/api/cases/<string:case_id>/messages/<string:message_id>')