"""JWT authentication middleware."""
from functools import wraps
from typing import Optional, Dict, Any
from flask import request, jsonify, g
import jwt
import os


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"


def get_token_from_header() -> Optional[str]:
    """Extract JWT token from Authorization header.

    Returns:
        Token string or None if not present
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    return parts[1]


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_current_user() -> Optional[Dict[str, Any]]:
    """Get current authenticated user from request context.

    Returns:
        User info dict or None if not authenticated
    """
    return getattr(g, "user", None)


def require_auth(f):
    """Decorator to require JWT authentication for route.

    Usage:
        @blueprint.route('/protected')
        @require_auth
        def protected_route():
            user = get_current_user()
            return jsonify({"user_id": user["user_id"]})

    Returns:
        Decorated function that validates JWT token
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()

        if not token:
            return (
                jsonify({"error": "Unauthorized", "message": "Missing authentication token"}),
                401,
            )

        payload = decode_token(token)

        if not payload:
            return (
                jsonify({"error": "Unauthorized", "message": "Invalid or expired token"}),
                401,
            )

        # Store user info in Flask g object for access in route
        g.user = {
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
        }

        return f(*args, **kwargs)

    return decorated_function
