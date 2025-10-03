"""Attribute service for business logic."""
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from ..repositories.attribute_repository import AttributeRepository
from ..repositories.entity_repository import EntityRepository


class AttributeService:
    """Service for Attribute business logic with data type validation."""

    def __init__(self, db: Session):
        """Initialize attribute service.

        Args:
            db: Database session
        """
        self.db = db
        self.repository = AttributeRepository(db)
        self.entity_repository = EntityRepository(db)

    def get_by_id(self, id: int) -> Optional[Dict]:
        """Get attribute by ID.

        Args:
            id: Attribute ID

        Returns:
            Attribute dict or None
        """
        attribute = self.repository.get(id)
        if not attribute:
            return None

        return self._to_dict(attribute)

    def list_by_entity(self, entity_id: int) -> Dict:
        """List attributes for an entity.

        Args:
            entity_id: Entity ID

        Returns:
            Dictionary with data list
        """
        # Verify entity exists
        entity = self.entity_repository.get(entity_id)
        if not entity:
            raise ValueError(f"Entity with ID {entity_id} not found")

        attributes = self.repository.get_by_entity(entity_id)

        return {"data": [self._to_dict(a) for a in attributes]}

    def create(self, entity_id: int, data: Dict, user_id: Optional[int] = None) -> Dict:
        """Create new attribute.

        Args:
            entity_id: Parent entity ID
            data: Attribute data (name, dataType, isNullable, etc.)
            user_id: Creator user ID

        Returns:
            Created attribute dict

        Raises:
            ValueError: If validation fails
        """
        # Verify entity exists
        entity = self.entity_repository.get(entity_id)
        if not entity:
            raise ValueError(f"Entity with ID {entity_id} not found")

        # Validation
        name = data.get("name", "").strip()
        if not name:
            raise ValueError("Attribute name is required")

        if len(name) > 100:
            raise ValueError("Attribute name must be 100 characters or less")

        # Check unique constraint: (entity_id, name)
        existing = self.repository.get_by_name_and_entity(name, entity_id)
        if existing:
            raise ValueError(
                f"Attribute with name '{name}' already exists in entity '{entity.name}'"
            )

        # Validate data type
        data_type = data.get("dataType")
        if not data_type:
            raise ValueError("Data type is required")

        if not self.repository.validate_data_type(data_type):
            from ..models.object_repository import Attribute

            valid_types = ", ".join(Attribute.VALID_DATA_TYPES)
            raise ValueError(
                f"Invalid data type '{data_type}'. Must be one of: {valid_types}"
            )

        # Create
        create_data = {
            "entity_id": entity_id,
            "name": name,
            "data_type": data_type,
            "is_nullable": data.get("isNullable", True),
            "default_value": data.get("defaultValue"),
            "description": data.get("description"),
            "constraints": data.get("constraints"),
            "data_quality_rules": data.get("dataQualityRules"),
            "created_by": user_id,
        }

        attribute = self.repository.create(create_data)
        return self._to_dict(attribute)

    def update(self, id: int, data: Dict) -> Optional[Dict]:
        """Update attribute.

        Args:
            id: Attribute ID
            data: Fields to update

        Returns:
            Updated attribute dict or None

        Raises:
            ValueError: If validation fails
        """
        attribute = self.repository.get(id)
        if not attribute:
            return None

        # Validation
        if "name" in data:
            name = data["name"].strip()
            if not name:
                raise ValueError("Attribute name cannot be empty")

            if len(name) > 100:
                raise ValueError("Attribute name must be 100 characters or less")

            # Check unique constraint (excluding current attribute)
            existing = self.repository.get_by_name_and_entity(name, attribute.entity_id)
            if existing and existing.id != id:
                raise ValueError(
                    f"Attribute with name '{name}' already exists in this entity"
                )

        if "dataType" in data:
            data_type = data["dataType"]
            if not self.repository.validate_data_type(data_type):
                from ..models.object_repository import Attribute

                valid_types = ", ".join(Attribute.VALID_DATA_TYPES)
                raise ValueError(
                    f"Invalid data type '{data_type}'. Must be one of: {valid_types}"
                )

        # Update
        updated = self.repository.update(id, data)
        return self._to_dict(updated) if updated else None

    def delete(self, id: int) -> Dict:
        """Delete attribute.

        Args:
            id: Attribute ID

        Returns:
            Success message

        Raises:
            ValueError: If attribute not found
        """
        attribute = self.repository.get(id)
        if not attribute:
            raise ValueError("Attribute not found")

        self.repository.delete(id)

        return {
            "message": f"Attribute '{attribute.name}' deleted successfully",
        }

    def _to_dict(self, attribute) -> Dict:
        """Convert attribute model to dictionary.

        Args:
            attribute: Attribute model instance

        Returns:
            Dictionary representation
        """
        return {
            "id": attribute.id,
            "entityId": attribute.entity_id,
            "name": attribute.name,
            "dataType": attribute.data_type,
            "isNullable": attribute.is_nullable,
            "defaultValue": attribute.default_value,
            "description": attribute.description,
            "constraints": attribute.constraints,
            "dataQualityRules": attribute.data_quality_rules,
            "createdAt": attribute.created_at.isoformat() if attribute.created_at else None,
            "updatedAt": attribute.updated_at.isoformat() if attribute.updated_at else None,
        }
