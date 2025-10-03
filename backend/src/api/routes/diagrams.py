"""Diagram routes."""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..middleware.auth import require_auth, get_current_user
from ..schemas.diagram import (
    DiagramCreate,
    DiagramUpdate,
    DiagramResponse,
    DiagramObjectCreate,
    DiagramObjectUpdate,
    DiagramObjectResponse,
)
from ...services.diagram_service import DiagramService
from ...utils.database import get_db

diagrams_bp = Blueprint("diagrams", __name__)


@diagrams_bp.route("", methods=["GET"])
@require_auth
def list_diagrams():
    """List all diagrams for current user.

    GET /api/v1/diagrams?skip=0&limit=100
    Response: [DiagramResponse, ...]
    """
    try:
        user = get_current_user()
        skip = request.args.get("skip", 0, type=int)
        limit = request.args.get("limit", 100, type=int)

        db: Session = next(get_db())
        try:
            service = DiagramService(db)
            diagrams = service.list_diagrams(user["user_id"], skip, limit)

            response = [DiagramResponse.model_validate(d) for d in diagrams]
            return jsonify(response), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@diagrams_bp.route("", methods=["POST"])
@require_auth
def create_diagram():
    """Create a new diagram.

    POST /api/v1/diagrams
    Request body: {
        "name": "Sales Overview",
        "description": "...",
        "tags": ["sales", "customer"],
        "canvas_settings": {...}
    }
    Response: DiagramResponse
    """
    try:
        user = get_current_user()
        data = DiagramCreate(**request.json)

        db: Session = next(get_db())
        try:
            service = DiagramService(db)
            diagram = service.create_diagram(
                user_id=user["user_id"],
                name=data.name,
                description=data.description,
                tags=data.tags,
                canvas_settings=data.canvas_settings,
            )

            response = DiagramResponse.model_validate(diagram)
            return jsonify(response.model_dump()), 201

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@diagrams_bp.route("/<int:id>", methods=["GET"])
@require_auth
def get_diagram(id: int):
    """Get diagram by ID with full details.

    GET /api/v1/diagrams/{id}
    Response: DiagramResponse (with objects and relationships)
    """
    try:
        user = get_current_user()

        db: Session = next(get_db())
        try:
            service = DiagramService(db)
            diagram = service.get_diagram(id, user["user_id"])

            if not diagram:
                return jsonify({"error": "Not Found", "message": "Diagram not found"}), 404

            response = DiagramResponse.model_validate(diagram)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@diagrams_bp.route("/<int:id>", methods=["PUT"])
@require_auth
def update_diagram(id: int):
    """Update diagram metadata.

    PUT /api/v1/diagrams/{id}
    Request body: {"name": "New Name", "description": "...", ...}
    Response: DiagramResponse
    """
    try:
        user = get_current_user()
        data = DiagramUpdate(**request.json)

        db: Session = next(get_db())
        try:
            service = DiagramService(db)
            diagram = service.update_diagram(
                id=id,
                user_id=user["user_id"],
                name=data.name,
                description=data.description,
                tags=data.tags,
                canvas_settings=data.canvas_settings,
            )

            if not diagram:
                return jsonify({"error": "Not Found", "message": "Diagram not found"}), 404

            response = DiagramResponse.model_validate(diagram)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@diagrams_bp.route("/<int:id>", methods=["DELETE"])
@require_auth
def delete_diagram(id: int):
    """Delete diagram.

    DELETE /api/v1/diagrams/{id}
    Response: {"message": "Diagram deleted"}
    """
    try:
        user = get_current_user()

        db: Session = next(get_db())
        try:
            service = DiagramService(db)
            success = service.delete_diagram(id, user["user_id"])

            if not success:
                return jsonify({"error": "Not Found", "message": "Diagram not found"}), 404

            return jsonify({"message": "Diagram deleted successfully"}), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


# Diagram Objects endpoints


@diagrams_bp.route("/<int:diagram_id>/objects", methods=["POST"])
@require_auth
def add_diagram_object(diagram_id: int):
    """Add an object to diagram.

    POST /api/v1/diagrams/{diagram_id}/objects
    Request body: {
        "object_type": "ENTITY",
        "object_id": 1,
        "position_x": 100,
        "position_y": 200,
        "visual_style": {...}
    }
    Response: DiagramObjectResponse
    """
    try:
        user = get_current_user()
        data = DiagramObjectCreate(**request.json)

        db: Session = next(get_db())
        try:
            service = DiagramService(db)
            diagram_object = service.add_object(
                diagram_id=diagram_id,
                user_id=user["user_id"],
                object_type=data.object_type,
                object_id=data.object_id,
                position_x=data.position_x,
                position_y=data.position_y,
                visual_style=data.visual_style,
            )

            response = DiagramObjectResponse.model_validate(diagram_object)
            return jsonify(response.model_dump()), 201

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@diagrams_bp.route("/<int:diagram_id>/objects/<int:object_id>", methods=["PUT"])
@require_auth
def update_diagram_object(diagram_id: int, object_id: int):
    """Update diagram object position or style.

    PUT /api/v1/diagrams/{diagram_id}/objects/{object_id}
    Request body: {"position_x": 150, "position_y": 250, "visual_style": {...}}
    Response: DiagramObjectResponse
    """
    try:
        user = get_current_user()
        data = DiagramObjectUpdate(**request.json)

        db: Session = next(get_db())
        try:
            service = DiagramService(db)
            diagram_object = service.update_object_position(
                diagram_id=diagram_id,
                object_id=object_id,
                user_id=user["user_id"],
                position_x=data.position_x,
                position_y=data.position_y,
                visual_style=data.visual_style,
            )

            if not diagram_object:
                return (
                    jsonify({"error": "Not Found", "message": "Diagram object not found"}),
                    404,
                )

            response = DiagramObjectResponse.model_validate(diagram_object)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@diagrams_bp.route("/<int:diagram_id>/objects/<int:object_id>", methods=["DELETE"])
@require_auth
def remove_diagram_object(diagram_id: int, object_id: int):
    """Remove object from diagram (doesn't delete from repository).

    DELETE /api/v1/diagrams/{diagram_id}/objects/{object_id}
    Response: {"message": "Object removed from diagram"}
    """
    try:
        user = get_current_user()

        db: Session = next(get_db())
        try:
            service = DiagramService(db)
            success = service.remove_object(
                diagram_id=diagram_id,
                object_id=object_id,
                user_id=user["user_id"],
            )

            if not success:
                return (
                    jsonify({"error": "Not Found", "message": "Diagram object not found"}),
                    404,
                )

            return jsonify({"message": "Object removed from diagram successfully"}), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
