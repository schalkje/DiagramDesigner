"""Attribute repository for data access."""
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.object_repository import Attribute
from .base_repository import BaseRepository


class AttributeRepository(BaseRepository[Attribute]):
    """Repository for Attribute entities with entity filtering and validation."""

    def __init__(self, db: Session):
        """Initialize attribute repository.

        Args:
            db: Database session
        """
        super().__init__(Attribute, db)

    def get_by_entity(self, entity_id: int) -> List[Attribute]:
        """Get all attributes for an entity.

        Args:
            entity_id: Parent entity ID

        Returns:
            List of Attribute instances
        """
        return (
            self.db.query(Attribute)
            .filter(Attribute.entity_id == entity_id)
            .order_by(Attribute.created_at)
            .all()
        )

    def get_by_name_and_entity(
        self, name: str, entity_id: int
    ) -> Optional[Attribute]:
        """Get attribute by name within an entity.

        Used for checking unique constraint: (entity_id, name).

        Args:
            name: Attribute name
            entity_id: Parent entity ID

        Returns:
            Attribute instance or None
        """
        return (
            self.db.query(Attribute)
            .filter(Attribute.name == name, Attribute.entity_id == entity_id)
            .first()
        )

    def count_by_entity(self, entity_id: int) -> int:
        """Count attributes for an entity.

        Args:
            entity_id: Parent entity ID

        Returns:
            Count of attributes
        """
        return self.db.query(Attribute).filter(Attribute.entity_id == entity_id).count()

    def validate_data_type(self, data_type: str) -> bool:
        """Validate that data_type is from allowed list.

        Args:
            data_type: Data type string

        Returns:
            True if valid, False otherwise
        """
        return data_type in Attribute.VALID_DATA_TYPES

    def get_by_data_type(
        self, entity_id: int, data_type: str
    ) -> List[Attribute]:
        """Get attributes by data type within an entity.

        Args:
            entity_id: Parent entity ID
            data_type: Data type to filter by

        Returns:
            List of Attribute instances
        """
        return (
            self.db.query(Attribute)
            .filter(
                Attribute.entity_id == entity_id,
                Attribute.data_type == data_type,
            )
            .all()
        )

    def get_nullable_attributes(self, entity_id: int) -> List[Attribute]:
        """Get all nullable attributes for an entity.

        Args:
            entity_id: Parent entity ID

        Returns:
            List of nullable Attribute instances
        """
        return (
            self.db.query(Attribute)
            .filter(
                Attribute.entity_id == entity_id,
                Attribute.is_nullable == True,
            )
            .all()
        )
