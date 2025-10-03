"""Base repository with generic CRUD operations."""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from ..models import Base

# Generic type for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations.

    This provides a generic interface for database operations that can be
    extended by specific repositories.
    """

    def __init__(self, model: Type[ModelType], db: Session):
        """Initialize repository.

        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[ModelType]:
        """Get entity by ID.

        Args:
            id: Primary key value

        Returns:
            Model instance or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def list(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[ModelType]:
        """List entities with pagination and optional filters.

        Args:
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return
            filters: Dictionary of field: value filters

        Returns:
            List of model instances
        """
        query = self.db.query(self.model)

        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)

        return query.offset(skip).limit(limit).all()

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count total entities matching filters.

        Args:
            filters: Dictionary of field: value filters

        Returns:
            Total count
        """
        query = self.db.query(self.model)

        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)

        return query.count()

    def create(self, data: Dict[str, Any]) -> ModelType:
        """Create new entity.

        Args:
            data: Dictionary of field values

        Returns:
            Created model instance
        """
        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id: int, data: Dict[str, Any]) -> Optional[ModelType]:
        """Update entity by ID.

        Args:
            id: Primary key value
            data: Dictionary of field values to update

        Returns:
            Updated model instance or None if not found
        """
        instance = self.get(id)
        if not instance:
            return None

        for field, value in data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)

        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        """Delete entity by ID.

        Args:
            id: Primary key value

        Returns:
            True if deleted, False if not found
        """
        instance = self.get(id)
        if not instance:
            return False

        self.db.delete(instance)
        self.db.commit()
        return True

    def exists(self, id: int) -> bool:
        """Check if entity exists by ID.

        Args:
            id: Primary key value

        Returns:
            True if exists, False otherwise
        """
        return self.db.query(self.model.id).filter(self.model.id == id).first() is not None
