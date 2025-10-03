"""Relationship repository for data access."""
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from ..models.relationship import Cardinality, Relationship
from .base_repository import BaseRepository


class RelationshipRepository(BaseRepository[Relationship]):
    """Repository for Relationship entities with entity filtering and validation."""

    def __init__(self, db: Session):
        """Initialize relationship repository.

        Args:
            db: Database session
        """
        super().__init__(Relationship, db)

    def get_by_entity(self, entity_id: int) -> List[Relationship]:
        """Get all relationships involving an entity (as source or target).

        Args:
            entity_id: Entity ID

        Returns:
            List of Relationship instances
        """
        return (
            self.db.query(Relationship)
            .filter(
                (Relationship.source_entity_id == entity_id)
                | (Relationship.target_entity_id == entity_id)
            )
            .all()
        )

    def get_by_source_entity(self, source_entity_id: int) -> List[Relationship]:
        """Get relationships where entity is the source.

        Args:
            source_entity_id: Source entity ID

        Returns:
            List of Relationship instances
        """
        return (
            self.db.query(Relationship)
            .filter(Relationship.source_entity_id == source_entity_id)
            .all()
        )

    def get_by_target_entity(self, target_entity_id: int) -> List[Relationship]:
        """Get relationships where entity is the target.

        Args:
            target_entity_id: Target entity ID

        Returns:
            List of Relationship instances
        """
        return (
            self.db.query(Relationship)
            .filter(Relationship.target_entity_id == target_entity_id)
            .all()
        )

    def get_between_entities(
        self, source_entity_id: int, target_entity_id: int
    ) -> List[Relationship]:
        """Get all relationships between two entities.

        Args:
            source_entity_id: Source entity ID
            target_entity_id: Target entity ID

        Returns:
            List of Relationship instances
        """
        return (
            self.db.query(Relationship)
            .filter(
                Relationship.source_entity_id == source_entity_id,
                Relationship.target_entity_id == target_entity_id,
            )
            .all()
        )

    def get_with_entities(self, id: int) -> Optional[Relationship]:
        """Get relationship by ID with source and target entities eagerly loaded.

        Args:
            id: Relationship ID

        Returns:
            Relationship instance with entities or None
        """
        return (
            self.db.query(Relationship)
            .options(
                joinedload(Relationship.source_entity),
                joinedload(Relationship.target_entity),
            )
            .filter(Relationship.id == id)
            .first()
        )

    def get_self_referential(self, entity_id: int) -> List[Relationship]:
        """Get self-referential relationships for an entity.

        Args:
            entity_id: Entity ID

        Returns:
            List of self-referential Relationship instances
        """
        return (
            self.db.query(Relationship)
            .filter(
                Relationship.source_entity_id == entity_id,
                Relationship.target_entity_id == entity_id,
            )
            .all()
        )

    def validate_cardinality(self, cardinality: str) -> bool:
        """Validate that cardinality is from allowed enum.

        Args:
            cardinality: Cardinality string

        Returns:
            True if valid, False otherwise
        """
        try:
            Cardinality(cardinality)
            return True
        except ValueError:
            return False

    def count_by_entity(self, entity_id: int) -> int:
        """Count relationships involving an entity.

        Args:
            entity_id: Entity ID

        Returns:
            Count of relationships
        """
        return (
            self.db.query(Relationship)
            .filter(
                (Relationship.source_entity_id == entity_id)
                | (Relationship.target_entity_id == entity_id)
            )
            .count()
        )
