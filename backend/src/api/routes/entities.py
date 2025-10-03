"""Entity routes."""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..middleware.auth import require_auth, get_current_user
from ..schemas.entity import EntityCreate, EntityUpdate, EntityResponse, EntityListResponse
from ...services.entity_service import EntityService
from ...utils.database import get_db

entities_bp = Blueprint("entities", __name__)


@entities_bp.route("", methods=["GET"])
@require_auth
def list_entities():
    """List entities, optionally filtered by domain.

    GET /api/v1/entities?domain_id=1&skip=0&limit=100
    Response: {"entities": [...], "total": 20}
    """
    try:
        user = get_current_user()
        domain_id = request.args.get("domain_id", type=int)
        skip = request.args.get("skip", 0, type=int)
        limit = request.args.get("limit", 100, type=int)

        db: Session = next(get_db())
        try:
            service = EntityService(db)
            entities = service.list_entities(user["user_id"], domain_id, skip, limit)
            total = service.count_entities(user["user_id"], domain_id)

            response = EntityListResponse(
                entities=[EntityResponse.model_validate(e) for e in entities],
                total=total,
            )
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@entities_bp.route("", methods=["POST"])
@require_auth
def create_entity():
    """Create a new entity.

    POST /api/v1/entities
    Request body: {"domain_id": 1, "name": "Customer", "description": "..."}
    Response: EntityResponse
    """
    try:
        user = get_current_user()
        data = EntityCreate(**request.json)

        db: Session = next(get_db())
        try:
            service = EntityService(db)
            entity = service.create_entity(
                user_id=user["user_id"],
                domain_id=data.domain_id,
                name=data.name,
                description=data.description,
            )

            response = EntityResponse.model_validate(entity)
            return jsonify(response.model_dump()), 201

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@entities_bp.route("/<int:id>", methods=["GET"])
@require_auth
def get_entity(id: int):
    """Get entity by ID.

    GET /api/v1/entities/{id}
    Response: EntityResponse
    """
    try:
        user = get_current_user()

        db: Session = next(get_db())
        try:
            service = EntityService(db)
            entity = service.get_entity(id, user["user_id"])

            if not entity:
                return jsonify({"error": "Not Found", "message": "Entity not found"}), 404

            response = EntityResponse.model_validate(entity)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@entities_bp.route("/<int:id>", methods=["PUT"])
@require_auth
def update_entity(id: int):
    """Update entity.

    PUT /api/v1/entities/{id}
    Request body: {"name": "New Name", "description": "..."}
    Response: EntityResponse
    """
    try:
        user = get_current_user()
        data = EntityUpdate(**request.json)

        db: Session = next(get_db())
        try:
            service = EntityService(db)
            entity = service.update_entity(
                id=id,
                user_id=user["user_id"],
                name=data.name,
                description=data.description,
            )

            if not entity:
                return jsonify({"error": "Not Found", "message": "Entity not found"}), 404

            response = EntityResponse.model_validate(entity)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@entities_bp.route("/<int:id>", methods=["DELETE"])
@require_auth
def delete_entity(id: int):
    """Delete entity with cascade.

    DELETE /api/v1/entities/{id}?confirm=true
    Response: {"message": "Entity deleted"}
    """
    try:
        user = get_current_user()
        confirm = request.args.get("confirm", "false").lower() == "true"

        db: Session = next(get_db())
        try:
            service = EntityService(db)
            success = service.delete_entity(id, user["user_id"], confirm=confirm)

            if not success:
                return jsonify({"error": "Not Found", "message": "Entity not found"}), 404

            return jsonify({"message": "Entity deleted successfully"}), 200

        finally:
            db.close()

    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
