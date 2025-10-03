"""Domain routes."""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..middleware.auth import require_auth, get_current_user
from ..schemas.domain import DomainCreate, DomainUpdate, DomainResponse, DomainListResponse
from ...services.domain_service import DomainService
from ...utils.database import get_db

domains_bp = Blueprint("domains", __name__)


@domains_bp.route("", methods=["GET"])
@require_auth
def list_domains():
    """List domains, optionally filtered by superdomain.

    GET /api/v1/domains?superdomain_id=1&skip=0&limit=100
    Response: {"domains": [...], "total": 5}
    """
    try:
        user = get_current_user()
        superdomain_id = request.args.get("superdomain_id", type=int)
        skip = request.args.get("skip", 0, type=int)
        limit = request.args.get("limit", 100, type=int)

        db: Session = next(get_db())
        try:
            service = DomainService(db)
            domains = service.list_domains(user["user_id"], superdomain_id, skip, limit)
            total = service.count_domains(user["user_id"], superdomain_id)

            response = DomainListResponse(
                domains=[DomainResponse.model_validate(d) for d in domains],
                total=total,
            )
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@domains_bp.route("", methods=["POST"])
@require_auth
def create_domain():
    """Create a new domain.

    POST /api/v1/domains
    Request body: {"superdomain_id": 1, "name": "Sales", "description": "..."}
    Response: DomainResponse
    """
    try:
        user = get_current_user()
        data = DomainCreate(**request.json)

        db: Session = next(get_db())
        try:
            service = DomainService(db)
            domain = service.create_domain(
                user_id=user["user_id"],
                superdomain_id=data.superdomain_id,
                name=data.name,
                description=data.description,
            )

            response = DomainResponse.model_validate(domain)
            return jsonify(response.model_dump()), 201

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@domains_bp.route("/<int:id>", methods=["GET"])
@require_auth
def get_domain(id: int):
    """Get domain by ID.

    GET /api/v1/domains/{id}
    Response: DomainResponse
    """
    try:
        user = get_current_user()

        db: Session = next(get_db())
        try:
            service = DomainService(db)
            domain = service.get_domain(id, user["user_id"])

            if not domain:
                return jsonify({"error": "Not Found", "message": "Domain not found"}), 404

            response = DomainResponse.model_validate(domain)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@domains_bp.route("/<int:id>", methods=["PUT"])
@require_auth
def update_domain(id: int):
    """Update domain.

    PUT /api/v1/domains/{id}
    Request body: {"name": "New Name", "description": "..."}
    Response: DomainResponse
    """
    try:
        user = get_current_user()
        data = DomainUpdate(**request.json)

        db: Session = next(get_db())
        try:
            service = DomainService(db)
            domain = service.update_domain(
                id=id,
                user_id=user["user_id"],
                name=data.name,
                description=data.description,
            )

            if not domain:
                return jsonify({"error": "Not Found", "message": "Domain not found"}), 404

            response = DomainResponse.model_validate(domain)
            return jsonify(response.model_dump()), 200

        finally:
            db.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@domains_bp.route("/<int:id>", methods=["DELETE"])
@require_auth
def delete_domain(id: int):
    """Delete domain with cascade.

    DELETE /api/v1/domains/{id}?confirm=true
    Response: {"message": "Domain deleted"}
    """
    try:
        user = get_current_user()
        confirm = request.args.get("confirm", "false").lower() == "true"

        db: Session = next(get_db())
        try:
            service = DomainService(db)
            success = service.delete_domain(id, user["user_id"], confirm=confirm)

            if not success:
                return jsonify({"error": "Not Found", "message": "Domain not found"}), 404

            return jsonify({"message": "Domain deleted successfully"}), 200

        finally:
            db.close()

    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
