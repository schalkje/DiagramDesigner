"""Authentication routes."""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from ...services.auth_service import AuthService
from ...utils.database import get_db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """User login endpoint.

    POST /api/v1/auth/login
    Request body: {"email": "user@example.com", "password": "password123"}
    Response: {"token": "jwt_token", "user": {...}}
    """
    try:
        # Validate request
        data = LoginRequest(**request.json)

        # Get database session
        db: Session = next(get_db())

        try:
            # Authenticate user
            auth_service = AuthService(db)
            result = auth_service.login(data.email, data.password)

            if not result:
                return (
                    jsonify({"error": "Unauthorized", "message": "Invalid credentials"}),
                    401,
                )

            # Return token and user info
            response = LoginResponse(**result)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@auth_bp.route("/register", methods=["POST"])
def register():
    """User registration endpoint.

    POST /api/v1/auth/register
    Request body: {
        "email": "user@example.com",
        "username": "username",
        "password": "password123",
        "full_name": "User Name"
    }
    Response: {"token": "jwt_token", "user": {...}}
    """
    try:
        # Validate request
        data = RegisterRequest(**request.json)

        # Get database session
        db: Session = next(get_db())

        try:
            # Register user
            auth_service = AuthService(db)
            result = auth_service.register(
                email=data.email,
                username=data.username,
                password=data.password,
                full_name=data.full_name,
            )

            # Return token and user info
            response = RegisterResponse(**result)
            return jsonify(response.model_dump()), 201

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
