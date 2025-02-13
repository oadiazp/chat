from jsonschema import validate, ValidationError
from schemas import SUPPORT_CASE_SCHEMA, MESSAGE_SCHEMA
import logging

logger = logging.getLogger(__name__)

def validate_support_case(data):
    try:
        validate(instance=data, schema=SUPPORT_CASE_SCHEMA)
        return True
    except ValidationError as e:
        logger.error(f"Support case validation error: {str(e)}")
        return False

def validate_message(data):
    try:
        validate(instance=data, schema=MESSAGE_SCHEMA)
        return True
    except ValidationError as e:
        logger.error(f"Message validation error: {str(e)}")
        return False
