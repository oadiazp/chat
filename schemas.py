SUPPORT_CASE_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string", "minLength": 1, "maxLength": 200},
        "description": {"type": "string", "minLength": 1},
        "customer_id": {"type": "integer", "minimum": 1}
    },
    "required": ["summary", "description", "customer_id"],
    "additionalProperties": False
}

MESSAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "content": {"type": "string", "minLength": 1}
    },
    "required": ["content"],
    "additionalProperties": False
}