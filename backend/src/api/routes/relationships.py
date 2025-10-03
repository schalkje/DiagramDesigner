"""Relationship routes."""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..middleware.auth import require_auth, get_current_user
from ..schemas.relationship import RelationshipCreate, RelationshipResponse
from ...services.relationship_service import RelationshipService
from ...utils.database import get_db

relationships_bp = Blueprint("relationships", __name__)


@relationships_bp.route("", methods=["GET"])
@require_auth
def list_relationships():
    """List relationships, optionally filtered by entity.

    GET /api/v1/relationships?entity_id=1
    Response: [RelationshipResponse, ...]
    """
    try:
        user = get_current_user()
        entity_id = request.args.get("entity_id", type=int)

        db: Session = next(get_db())
        try:
            service = RelationshipService(db)
            relationships = service.list_relationships(user["user_id"], entity_id)

            response = [RelationshipResponse.model_validate(r) for r in relationships]
            return jsonify(response), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@relationships_bp.route("", methods=["POST"])
@require_auth
def create_relationship():
    """Create a new relationship between entities.

    POST /api/v1/relationships
    Request body: {
        "source_entity_id": 1,
        "target_entity_id": 2,
        "source_role": "customer",
        "target_role": "orders",
        "source_cardinality": "ONE",
        "target_cardinality": "ZERO_MANY"
    }
    Response: RelationshipResponse
    """
    try:
        user = get_current_user()
        data = RelationshipCreate(**request.json)

        db: Session = next(get_db())
        try:
            service = RelationshipService(db)
            relationship = service.create_relationship(
                user_id=user["user_id"],
                source_entity_id=data.source_entity_id,
                target_entity_id=data.target_entity_id,
                source_role=data.source_role,
                target_role=data.target_role,
                source_cardinality=data.source_cardinality,
                target_cardinality=data.target_cardinality,
                description=data.description,
            )

            response = RelationshipResponse.model_validate(relationship)
            return jsonify(response.model_dump()), 201

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@relationships_bp.route("/<int:id>", methods=["GET"])
@require_auth
def get_relationship(id: int):
    """Get relationship by ID.

    GET /api/v1/relationships/{id}
    Response: RelationshipResponse
    """
    try:
        user = get_current_user()

        db: Session = next(get_db())
        try:
            service = RelationshipService(db)
            relationship = service.get_relationship(id, user["user_id"])

            if not relationship:
                return (
                    jsonify({"error": "Not Found", "message": "Relationship not found"}),
                    404,
                )

            response = RelationshipResponse.model_validate(relationship)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@relationships_bp.route("/<int:id>", methods=["DELETE"])
@require_auth
def delete_relationship(id: int):
    """Delete relationship.

    DELETE /api/v1/relationships/{id}
    Response: {"message": "Relationship deleted"}
    """
    try:
        user = get_current_user()

        db: Session = next(get_db())
        try:
            service = RelationshipService(db)
            success = service.delete_relationship(id, user["user_id"])

            if not success:
                return (
                    jsonify({"error": "Not Found", "message": "Relationship not found"}),
                    404,
                )

            return jsonify({"message": "Relationship deleted successfully"}), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
