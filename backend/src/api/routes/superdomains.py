"""Superdomain routes."""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..middleware.auth import require_auth, get_current_user
from ..schemas.superdomain import (
    SuperdomainCreate,
    SuperdomainUpdate,
    SuperdomainResponse,
    SuperdomainListResponse,
)
from ...services.superdomain_service import SuperdomainService
from ...utils.database import get_db

superdomains_bp = Blueprint("superdomains", __name__)


@superdomains_bp.route("", methods=["GET"])
@require_auth
def list_superdomains():
    """List all superdomains for current user.

    GET /api/v1/superdomains?skip=0&limit=100
    Response: {"superdomains": [...], "total": 10}
    """
    try:
        user = get_current_user()
        skip = request.args.get("skip", 0, type=int)
        limit = request.args.get("limit", 100, type=int)

        db: Session = next(get_db())
        try:
            service = SuperdomainService(db)
            superdomains = service.list_superdomains(user["user_id"], skip, limit)
            total = service.count_superdomains(user["user_id"])

            response = SuperdomainListResponse(
                superdomains=[SuperdomainResponse.model_validate(s) for s in superdomains],
                total=total,
            )
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@superdomains_bp.route("", methods=["POST"])
@require_auth
def create_superdomain():
    """Create a new superdomain.

    POST /api/v1/superdomains
    Request body: {"name": "Business", "description": "..."}
    Response: SuperdomainResponse
    """
    try:
        user = get_current_user()
        data = SuperdomainCreate(**request.json)

        db: Session = next(get_db())
        try:
            service = SuperdomainService(db)
            superdomain = service.create_superdomain(
                user_id=user["user_id"],
                name=data.name,
                description=data.description,
            )

            response = SuperdomainResponse.model_validate(superdomain)
            return jsonify(response.model_dump()), 201

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@superdomains_bp.route("/<int:id>", methods=["GET"])
@require_auth
def get_superdomain(id: int):
    """Get superdomain by ID.

    GET /api/v1/superdomains/{id}
    Response: SuperdomainResponse
    """
    try:
        user = get_current_user()

        db: Session = next(get_db())
        try:
            service = SuperdomainService(db)
            superdomain = service.get_superdomain(id, user["user_id"])

            if not superdomain:
                return jsonify({"error": "Not Found", "message": "Superdomain not found"}), 404

            response = SuperdomainResponse.model_validate(superdomain)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@superdomains_bp.route("/<int:id>", methods=["PUT"])
@require_auth
def update_superdomain(id: int):
    """Update superdomain.

    PUT /api/v1/superdomains/{id}
    Request body: {"name": "New Name", "description": "..."}
    Response: SuperdomainResponse
    """
    try:
        user = get_current_user()
        data = SuperdomainUpdate(**request.json)

        db: Session = next(get_db())
        try:
            service = SuperdomainService(db)
            superdomain = service.update_superdomain(
                id=id,
                user_id=user["user_id"],
                name=data.name,
                description=data.description,
            )

            if not superdomain:
                return jsonify({"error": "Not Found", "message": "Superdomain not found"}), 404

            response = SuperdomainResponse.model_validate(superdomain)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@superdomains_bp.route("/<int:id>", methods=["DELETE"])
@require_auth
def delete_superdomain(id: int):
    """Delete superdomain with cascade.

    DELETE /api/v1/superdomains/{id}?confirm=true
    Response: {"message": "Superdomain deleted", "impact": {...}}
    """
    try:
        user = get_current_user()
        confirm = request.args.get("confirm", "false").lower() == "true"

        db: Session = next(get_db())
        try:
            service = SuperdomainService(db)

            # Analyze impact
            impact = service.analyze_delete_impact(id, user["user_id"])

            if not confirm and impact.get("cascade"):
                return (
                    jsonify(
                        {
                            "error": "Confirmation Required",
                            "message": "Cascade delete requires confirmation",
                            "impact": impact,
                        }
                    ),
                    400,
                )

            # Delete
            success = service.delete_superdomain(id, user["user_id"], confirm=confirm)

            if not success:
                return jsonify({"error": "Not Found", "message": "Superdomain not found"}), 404

            return (
                jsonify({"message": "Superdomain deleted successfully", "impact": impact}),
                200,
            )

        finally:
            db.close()

    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
