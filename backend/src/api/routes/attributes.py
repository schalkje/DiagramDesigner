"""Attribute routes."""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..middleware.auth import require_auth, get_current_user
from ..schemas.attribute import (
    AttributeCreate,
    AttributeUpdate,
    AttributeResponse,
    AttributeListResponse,
)
from ...services.attribute_service import AttributeService
from ...utils.database import get_db

attributes_bp = Blueprint("attributes", __name__)


@attributes_bp.route("", methods=["GET"])
@require_auth
def list_attributes():
    """List attributes, optionally filtered by entity.

    GET /api/v1/attributes?entity_id=1&skip=0&limit=100
    Response: {"attributes": [...], "total": 15}
    """
    try:
        user = get_current_user()
        entity_id = request.args.get("entity_id", type=int)
        skip = request.args.get("skip", 0, type=int)
        limit = request.args.get("limit", 100, type=int)

        db: Session = next(get_db())
        try:
            service = AttributeService(db)
            attributes = service.list_attributes(user["user_id"], entity_id, skip, limit)
            total = service.count_attributes(user["user_id"], entity_id)

            response = AttributeListResponse(
                attributes=[AttributeResponse.model_validate(a) for a in attributes],
                total=total,
            )
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@attributes_bp.route("", methods=["POST"])
@require_auth
def create_attribute():
    """Create a new attribute.

    POST /api/v1/attributes
    Request body: {
        "entity_id": 1,
        "name": "email",
        "data_type": "String",
        "is_nullable": false,
        "is_primary_key": false
    }
    Response: AttributeResponse
    """
    try:
        user = get_current_user()
        data = AttributeCreate(**request.json)

        db: Session = next(get_db())
        try:
            service = AttributeService(db)
            attribute = service.create_attribute(
                user_id=user["user_id"],
                entity_id=data.entity_id,
                name=data.name,
                data_type=data.data_type,
                is_nullable=data.is_nullable,
                is_primary_key=data.is_primary_key,
                default_value=data.default_value,
                constraints=data.constraints,
            )

            response = AttributeResponse.model_validate(attribute)
            return jsonify(response.model_dump()), 201

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@attributes_bp.route("/<int:id>", methods=["GET"])
@require_auth
def get_attribute(id: int):
    """Get attribute by ID.

    GET /api/v1/attributes/{id}
    Response: AttributeResponse
    """
    try:
        user = get_current_user()

        db: Session = next(get_db())
        try:
            service = AttributeService(db)
            attribute = service.get_attribute(id, user["user_id"])

            if not attribute:
                return jsonify({"error": "Not Found", "message": "Attribute not found"}), 404

            response = AttributeResponse.model_validate(attribute)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@attributes_bp.route("/<int:id>", methods=["PUT"])
@require_auth
def update_attribute(id: int):
    """Update attribute.

    PUT /api/v1/attributes/{id}
    Request body: {"name": "new_name", "data_type": "Integer", ...}
    Response: AttributeResponse
    """
    try:
        user = get_current_user()
        data = AttributeUpdate(**request.json)

        db: Session = next(get_db())
        try:
            service = AttributeService(db)
            attribute = service.update_attribute(
                id=id,
                user_id=user["user_id"],
                name=data.name,
                data_type=data.data_type,
                is_nullable=data.is_nullable,
                is_primary_key=data.is_primary_key,
                default_value=data.default_value,
                constraints=data.constraints,
            )

            if not attribute:
                return jsonify({"error": "Not Found", "message": "Attribute not found"}), 404

            response = AttributeResponse.model_validate(attribute)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@attributes_bp.route("/<int:id>", methods=["DELETE"])
@require_auth
def delete_attribute(id: int):
    """Delete attribute.

    DELETE /api/v1/attributes/{id}
    Response: {"message": "Attribute deleted"}
    """
    try:
        user = get_current_user()

        db: Session = next(get_db())
        try:
            service = AttributeService(db)
            success = service.delete_attribute(id, user["user_id"])

            if not success:
                return jsonify({"error": "Not Found", "message": "Attribute not found"}), 404

            return jsonify({"message": "Attribute deleted successfully"}), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
