"""Entity service for business logic."""
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from ..repositories.domain_repository import DomainRepository
from ..repositories.entity_repository import EntityRepository
from ..repositories.relationship_repository import RelationshipRepository


class EntityService:
    """Service for Entity business logic with validation and cascade checks."""

    def __init__(self, db: Session):
        """Initialize entity service.

        Args:
            db: Database session
        """
        self.db = db
        self.repository = EntityRepository(db)
        self.domain_repository = DomainRepository(db)
        self.relationship_repository = RelationshipRepository(db)

    def get_by_id(self, id: int, include_attributes: bool = False) -> Optional[Dict]:
        """Get entity by ID.

        Args:
            id: Entity ID
            include_attributes: Whether to include attributes

        Returns:
            Entity dict or None
        """
        if include_attributes:
            entity = self.repository.get_with_attributes(id)
        else:
            entity = self.repository.get(id)

        if not entity:
            return None

        return self._to_dict(entity, include_attributes=include_attributes)

    def list(
        self,
        page: int = 1,
        page_size: int = 100,
        domain_id: Optional[int] = None,
    ) -> Dict:
        """List entities with pagination and optional filtering.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            domain_id: Optional domain filter

        Returns:
            Dictionary with data and pagination info
        """
        skip = (page - 1) * page_size

        if domain_id:
            entities = self.repository.get_by_domain(domain_id, skip=skip, limit=page_size)
            total = self.repository.count_by_domain(domain_id)
        else:
            entities = self.repository.list(skip=skip, limit=page_size)
            total = self.repository.count()

        return {
            "data": [self._to_dict(e) for e in entities],
            "pagination": {
                "page": page,
                "pageSize": page_size,
                "total": total,
                "totalPages": (total + page_size - 1) // page_size,
            },
        }

    def create(self, data: Dict, user_id: Optional[int] = None) -> Dict:
        """Create new entity.

        Args:
            data: Entity data (domainId, name, description)
            user_id: Creator user ID

        Returns:
            Created entity dict

        Raises:
            ValueError: If validation fails
        """
        # Validation
        domain_id = data.get("domainId")
        if not domain_id:
            raise ValueError("Domain ID is required")

        # Verify domain exists
        domain = self.domain_repository.get(domain_id)
        if not domain:
            raise ValueError(f"Domain with ID {domain_id} not found")

        name = data.get("name", "").strip()
        if not name:
            raise ValueError("Entity name is required")

        if len(name) > 100:
            raise ValueError("Entity name must be 100 characters or less")

        # Check unique constraint: (domain_id, name)
        existing = self.repository.get_by_name_and_domain(name, domain_id)
        if existing:
            raise ValueError(
                f"Entity with name '{name}' already exists in domain '{domain.name}'"
            )

        # Create
        create_data = {
            "domain_id": domain_id,
            "name": name,
            "description": data.get("description"),
            "created_by": user_id,
        }

        entity = self.repository.create(create_data)
        return self._to_dict(entity)

    def update(self, id: int, data: Dict) -> Optional[Dict]:
        """Update entity.

        Args:
            id: Entity ID
            data: Fields to update

        Returns:
            Updated entity dict or None

        Raises:
            ValueError: If validation fails
        """
        entity = self.repository.get(id)
        if not entity:
            return None

        # Validation
        if "name" in data:
            name = data["name"].strip()
            if not name:
                raise ValueError("Entity name cannot be empty")

            if len(name) > 100:
                raise ValueError("Entity name must be 100 characters or less")

            # Check unique constraint (excluding current entity)
            existing = self.repository.get_by_name_and_domain(name, entity.domain_id)
            if existing and existing.id != id:
                raise ValueError(f"Entity with name '{name}' already exists in this domain")

        # Update
        updated = self.repository.update(id, data)
        return self._to_dict(updated) if updated else None

    def delete(self, id: int) -> Dict:
        """Delete entity with relationship check.

        Args:
            id: Entity ID

        Returns:
            Delete impact report

        Raises:
            ValueError: If entity not found
        """
        entity = self.repository.get(id)
        if not entity:
            raise ValueError("Entity not found")

        # Check for relationships
        relationships = self.relationship_repository.get_by_entity(id)
        relationship_count = len(relationships)

        # Delete (cascade will handle attributes and relationships)
        self.repository.delete(id)

        return {
            "message": f"Entity '{entity.name}' deleted successfully",
            "affectedRelationships": [
                f"{r.source_entity.name} -> {r.target_entity.name}"
                for r in relationships
            ],
            "cascade": True,
        }

    def _to_dict(self, entity, include_attributes: bool = False) -> Dict:
        """Convert entity model to dictionary.

        Args:
            entity: Entity model instance
            include_attributes: Whether to include attributes

        Returns:
            Dictionary representation
        """
        result = {
            "id": entity.id,
            "domainId": entity.domain_id,
            "name": entity.name,
            "description": entity.description,
            "createdAt": entity.created_at.isoformat() if entity.created_at else None,
            "updatedAt": entity.updated_at.isoformat() if entity.updated_at else None,
        }

        if include_attributes and hasattr(entity, "attributes"):
            result["attributes"] = [
                {
                    "id": attr.id,
                    "name": attr.name,
                    "dataType": attr.data_type,
                    "isNullable": attr.is_nullable,
                }
                for attr in entity.attributes
            ]

        return result
