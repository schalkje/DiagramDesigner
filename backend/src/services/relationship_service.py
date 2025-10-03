"""Relationship service for business logic."""
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from ..models.relationship import Cardinality
from ..repositories.entity_repository import EntityRepository
from ..repositories.relationship_repository import RelationshipRepository


class RelationshipService:
    """Service for Relationship business logic with cardinality validation."""

    def __init__(self, db: Session):
        """Initialize relationship service.

        Args:
            db: Database session
        """
        self.db = db
        self.repository = RelationshipRepository(db)
        self.entity_repository = EntityRepository(db)

    def get_by_id(self, id: int) -> Optional[Dict]:
        """Get relationship by ID.

        Args:
            id: Relationship ID

        Returns:
            Relationship dict or None
        """
        relationship = self.repository.get_with_entities(id)
        if not relationship:
            return None

        return self._to_dict(relationship)

    def list(self, entity_id: Optional[int] = None) -> Dict:
        """List relationships with optional entity filter.

        Args:
            entity_id: Optional entity ID filter

        Returns:
            Dictionary with data list
        """
        if entity_id:
            relationships = self.repository.get_by_entity(entity_id)
        else:
            relationships = self.repository.list(limit=1000)  # Large limit for relationships

        return {"data": [self._to_dict(r) for r in relationships]}

    def create(self, data: Dict, user_id: Optional[int] = None) -> Dict:
        """Create new relationship.

        Args:
            data: Relationship data
            user_id: Creator user ID

        Returns:
            Created relationship dict

        Raises:
            ValueError: If validation fails
        """
        # Validation
        source_entity_id = data.get("sourceEntityId")
        target_entity_id = data.get("targetEntityId")

        if not source_entity_id:
            raise ValueError("Source entity ID is required")

        if not target_entity_id:
            raise ValueError("Target entity ID is required")

        # Verify entities exist
        source_entity = self.entity_repository.get(source_entity_id)
        if not source_entity:
            raise ValueError(f"Source entity with ID {source_entity_id} not found")

        target_entity = self.entity_repository.get(target_entity_id)
        if not target_entity:
            raise ValueError(f"Target entity with ID {target_entity_id} not found")

        # Validate cardinalities
        source_cardinality = data.get("sourceCardinality")
        target_cardinality = data.get("targetCardinality")

        if not source_cardinality:
            raise ValueError("Source cardinality is required")

        if not target_cardinality:
            raise ValueError("Target cardinality is required")

        if not self.repository.validate_cardinality(source_cardinality):
            raise ValueError(
                f"Invalid source cardinality '{source_cardinality}'. "
                f"Must be one of: ZERO_ONE, ONE, ZERO_MANY, ONE_MANY"
            )

        if not self.repository.validate_cardinality(target_cardinality):
            raise ValueError(
                f"Invalid target cardinality '{target_cardinality}'. "
                f"Must be one of: ZERO_ONE, ONE, ZERO_MANY, ONE_MANY"
            )

        # Check if multiple relationships exist between same entities
        existing = self.repository.get_between_entities(source_entity_id, target_entity_id)
        if len(existing) > 0:
            # Multiple relationships allowed but require unique roles
            source_role = data.get("sourceRole")
            target_role = data.get("targetRole")

            if not source_role or not target_role:
                raise ValueError(
                    "Multiple relationships between same entities require unique source and target roles"
                )

        # Create
        create_data = {
            "source_entity_id": source_entity_id,
            "target_entity_id": target_entity_id,
            "source_role": data.get("sourceRole"),
            "target_role": data.get("targetRole"),
            "source_cardinality": Cardinality(source_cardinality),
            "target_cardinality": Cardinality(target_cardinality),
            "name": data.get("name"),
            "description": data.get("description"),
            "created_by": user_id,
        }

        relationship = self.repository.create(create_data)
        return self._to_dict(relationship)

    def update(self, id: int, data: Dict) -> Optional[Dict]:
        """Update relationship.

        Args:
            id: Relationship ID
            data: Fields to update

        Returns:
            Updated relationship dict or None

        Raises:
            ValueError: If validation fails
        """
        relationship = self.repository.get(id)
        if not relationship:
            return None

        # Validate cardinalities if provided
        if "sourceCardinality" in data:
            if not self.repository.validate_cardinality(data["sourceCardinality"]):
                raise ValueError(f"Invalid source cardinality '{data['sourceCardinality']}'")
            data["source_cardinality"] = Cardinality(data.pop("sourceCardinality"))

        if "targetCardinality" in data:
            if not self.repository.validate_cardinality(data["targetCardinality"]):
                raise ValueError(f"Invalid target cardinality '{data['targetCardinality']}'")
            data["target_cardinality"] = Cardinality(data.pop("targetCardinality"))

        # Update
        updated = self.repository.update(id, data)
        return self._to_dict(updated) if updated else None

    def delete(self, id: int) -> Dict:
        """Delete relationship.

        Args:
            id: Relationship ID

        Returns:
            Success message

        Raises:
            ValueError: If relationship not found
        """
        relationship = self.repository.get(id)
        if not relationship:
            raise ValueError("Relationship not found")

        self.repository.delete(id)

        return {
            "message": "Relationship deleted successfully",
        }

    def _to_dict(self, relationship) -> Dict:
        """Convert relationship model to dictionary.

        Args:
            relationship: Relationship model instance

        Returns:
            Dictionary representation
        """
        return {
            "id": relationship.id,
            "sourceEntityId": relationship.source_entity_id,
            "targetEntityId": relationship.target_entity_id,
            "sourceRole": relationship.source_role,
            "targetRole": relationship.target_role,
            "sourceCardinality": relationship.source_cardinality.value,
            "targetCardinality": relationship.target_cardinality.value,
            "name": relationship.name,
            "description": relationship.description,
            "createdAt": relationship.created_at.isoformat()
            if relationship.created_at
            else None,
            "updatedAt": relationship.updated_at.isoformat()
            if relationship.updated_at
            else None,
        }
