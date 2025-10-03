"""Entity repository for data access."""
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from ..models.object_repository import Entity
from .base_repository import BaseRepository


class EntityRepository(BaseRepository[Entity]):
    """Repository for Entity entities with domain filtering and attribute loading."""

    def __init__(self, db: Session):
        """Initialize entity repository.

        Args:
            db: Database session
        """
        super().__init__(Entity, db)

    def get_by_domain(
        self, domain_id: int, skip: int = 0, limit: int = 100
    ) -> List[Entity]:
        """Get entities by domain ID.

        Args:
            domain_id: Parent domain ID
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            List of Entity instances
        """
        return (
            self.db.query(Entity)
            .filter(Entity.domain_id == domain_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_with_attributes(self, id: int) -> Optional[Entity]:
        """Get entity by ID with attributes eagerly loaded.

        Args:
            id: Entity ID

        Returns:
            Entity instance with attributes or None
        """
        return (
            self.db.query(Entity)
            .options(joinedload(Entity.attributes))
            .filter(Entity.id == id)
            .first()
        )

    def get_by_name_and_domain(self, name: str, domain_id: int) -> Optional[Entity]:
        """Get entity by name within a domain.

        Used for checking unique constraint: (domain_id, name).

        Args:
            name: Entity name
            domain_id: Parent domain ID

        Returns:
            Entity instance or None
        """
        return (
            self.db.query(Entity)
            .filter(Entity.name == name, Entity.domain_id == domain_id)
            .first()
        )

    def count_by_domain(self, domain_id: int) -> int:
        """Count entities in a domain.

        Args:
            domain_id: Parent domain ID

        Returns:
            Count of entities
        """
        return self.db.query(Entity).filter(Entity.domain_id == domain_id).count()

    def search_by_name(self, search_term: str, limit: int = 50) -> List[Entity]:
        """Search entities by name (case-insensitive partial match).

        Args:
            search_term: Search term
            limit: Maximum records to return

        Returns:
            List of matching Entity instances
        """
        return (
            self.db.query(Entity)
            .filter(Entity.name.ilike(f"%{search_term}%"))
            .limit(limit)
            .all()
        )
