# Support Case Management System

A Flask-based REST API designed for efficient support case management, providing robust handling of support interactions and associated chat messages. Built following Domain-Driven Design principles.

## Features

- Support case creation and management
- Message threading for each support case
- Pagination for message retrieval
- Health check endpoint
- RESTful API design
- Domain-driven architecture

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- pip (Python package manager)

## Installation & Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd support-case-management
```

2. Install required packages:
```bash
uv sync
```

3. Set up environment variables:
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/dbname"
export FLASK_SECRET_KEY="your-secret-key"
```

4. Initialize the database:
The application will automatically create the necessary tables when started for the first time.

## Development

### Running the Development Server

Start the Flask development server:
```bash
python main.py
```

The server will start on `http://localhost:5000`

### Running Tests

Execute the test suite:
```bash
python -m unittest discover -v tests
```

## API Documentation

### Health Check
- `GET /` - Redirects to health check
- `GET /health` - Check system health
  - Response: `{"status": "healthy", "database": "connected", "timestamp": "..."}`

### Support Cases
- `GET /api/cases` - List all support cases
- `GET /api/cases/<uuid>` - Get specific support case
- `POST /api/cases` - Create new support case
  ```json
  {
    "summary": "Issue description",
    "description": "Detailed description",
    "customer_id": 1
  }
  ```
- `PUT /api/cases/<uuid>` - Update support case
- `DELETE /api/cases/<uuid>` - Delete support case

### Messages
- `GET /api/cases/<case_uuid>/messages` - List messages for a case
  - Query parameters:
    - `limit` (optional, default: 10)
    - `offset` (optional, default: 0)
- `POST /api/cases/<case_uuid>/messages` - Add message to case
  ```json
  {
    "content": "Message content"
  }
  ```
- `DELETE /api/cases/<case_uuid>/messages/<message_uuid>` - Delete message

## Project Structure

```
├── application/         # Application services and use cases
├── domain/             # Domain entities and repository interfaces
├── infrastructure/     # Implementation details (database, API routes)
├── tests/             # Test suites
├── app.py             # Application configuration
└── main.py            # Entry point
```

### Domain-Driven Design Implementation

The project follows DDD principles with clear separation of:
- Domain Layer: Core business logic and rules
- Application Layer: Use cases and services
- Infrastructure Layer: Technical implementations

## Testing

The project includes comprehensive test coverage:
- Unit tests for domain logic
- Integration tests for API endpoints
- Health check verification
- Message pagination and ordering tests

## Error Handling

The API implements consistent error responses:
- 400: Bad Request (invalid input)
- 404: Resource Not Found
- 500: Internal Server Error

All errors return JSON responses with an `error` field containing the error message.