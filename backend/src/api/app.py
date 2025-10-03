"""Flask application factory."""
from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    """Create and configure Flask application.

    Returns:
        Flask app instance
    """
    app = Flask(__name__)

    # Configuration
    app.config["JSON_SORT_KEYS"] = False
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    register_blueprints(app)

    # Health check endpoint
    @app.route("/health")
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy"}), 200

    # Handle OPTIONS requests for CORS preflight
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    return app


def register_error_handlers(app):
    """Register error handlers.

    Args:
        app: Flask app instance
    """

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors."""
        return (
            jsonify({"error": "Unauthorized", "message": "Authentication required"}),
            401,
        )

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        return (
            jsonify({"error": "Internal Server Error", "message": "An error occurred"}),
            500,
        )

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        """Handle ValueError exceptions."""
        return jsonify({"error": "Validation Error", "message": str(error)}), 400


def register_blueprints(app):
    """Register Flask blueprints for routes.

    Args:
        app: Flask app instance
    """
    from .routes.auth import auth_bp
    from .routes.superdomains import superdomains_bp
    from .routes.domains import domains_bp
    from .routes.entities import entities_bp
    from .routes.attributes import attributes_bp
    from .routes.relationships import relationships_bp
    from .routes.diagrams import diagrams_bp

    # Register all blueprints with /api/v1 prefix
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(superdomains_bp, url_prefix="/api/v1/superdomains")
    app.register_blueprint(domains_bp, url_prefix="/api/v1/domains")
    app.register_blueprint(entities_bp, url_prefix="/api/v1/entities")
    app.register_blueprint(attributes_bp, url_prefix="/api/v1/attributes")
    app.register_blueprint(relationships_bp, url_prefix="/api/v1/relationships")
    app.register_blueprint(diagrams_bp, url_prefix="/api/v1/diagrams")
