import os
from flask import Flask
from flask_restful import Api
import logging
from infrastructure.database import db

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask application
app = Flask(__name__)
api = Api(app)

# Configure the application
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev_key")

# Initialize extensions with app
db.init_app(app)

# Initialize application context and create tables
with app.app_context():
    # Create all database tables
    db.create_all()

    # Import and initialize routes after models are ready
    from infrastructure.routes import initialize_routes
    initialize_routes(api)
    logger.info("Database tables created and routes initialized successfully")

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {"error": "Resource not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)