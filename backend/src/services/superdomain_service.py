"""Superdomain service for business logic."""
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from ..repositories.superdomain_repository import SuperdomainRepository


class SuperdomainService:
    """Service for Superdomain business logic with cascade delete and validation."""

    def __init__(self, db: Session):
        """Initialize superdomain service.

        Args:
            db: Database session
        """
        self.db = db
        self.repository = SuperdomainRepository(db)

    def get_by_id(self, id: int) -> Optional[Dict]:
        """Get superdomain by ID.

        Args:
            id: Superdomain ID

        Returns:
            Superdomain dict or None
        """
        superdomain = self.repository.get(id)
        if not superdomain:
            return None

        return self._to_dict(superdomain)

    def list(self, page: int = 1, page_size: int = 100) -> Dict:
        """List superdomains with pagination.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            Dictionary with data and pagination info
        """
        skip = (page - 1) * page_size
        superdomains = self.repository.list(skip=skip, limit=page_size)
        total = self.repository.count()

        return {
            "data": [self._to_dict(s) for s in superdomains],
            "pagination": {
                "page": page,
                "pageSize": page_size,
                "total": total,
                "totalPages": (total + page_size - 1) // page_size,
            },
        }

    def create(self, data: Dict, user_id: Optional[int] = None) -> Dict:
        """Create new superdomain.

        Args:
            data: Superdomain data (name, description)
            user_id: Creator user ID

        Returns:
            Created superdomain dict

        Raises:
            ValueError: If name is empty or already exists
        """
        # Validation
        name = data.get("name", "").strip()
        if not name:
            raise ValueError("Superdomain name is required")

        if len(name) > 100:
            raise ValueError("Superdomain name must be 100 characters or less")

        # Check unique constraint
        existing = self.repository.get_by_name(name)
        if existing:
            raise ValueError(f"Superdomain with name '{name}' already exists")

        # Create
        create_data = {
            "name": name,
            "description": data.get("description"),
            "created_by": user_id,
        }

        superdomain = self.repository.create(create_data)
        return self._to_dict(superdomain)

    def update(self, id: int, data: Dict) -> Optional[Dict]:
        """Update superdomain.

        Args:
            id: Superdomain ID
            data: Fields to update

        Returns:
            Updated superdomain dict or None

        Raises:
            ValueError: If validation fails
        """
        superdomain = self.repository.get(id)
        if not superdomain:
            return None

        # Validation
        if "name" in data:
            name = data["name"].strip()
            if not name:
                raise ValueError("Superdomain name cannot be empty")

            if len(name) > 100:
                raise ValueError("Superdomain name must be 100 characters or less")

            # Check unique constraint (excluding current superdomain)
            existing = self.repository.get_by_name(name)
            if existing and existing.id != id:
                raise ValueError(f"Superdomain with name '{name}' already exists")

        # Update
        updated = self.repository.update(id, data)
        return self._to_dict(updated) if updated else None

    def delete(self, id: int, confirm_cascade: bool = False) -> Dict:
        """Delete superdomain with cascade impact analysis.

        Args:
            id: Superdomain ID
            confirm_cascade: Whether user confirmed cascade delete

        Returns:
            Delete impact report

        Raises:
            ValueError: If superdomain not found or cascade not confirmed
        """
        superdomain = self.repository.get(id)
        if not superdomain:
            raise ValueError("Superdomain not found")

        # Analyze impact
        impact = self.repository.analyze_delete_impact(id)

        # If there are affected entities and cascade not confirmed, return impact
        if impact["cascade"] and not confirm_cascade:
            return {
                "message": f"Superdomain '{superdomain.name}' has dependencies",
                "affectedDomains": impact["affected_domains"],
                "affectedEntities": impact["affected_entities"],
                "cascade": True,
                "requiresConfirmation": True,
            }

        # Perform delete (cascade handled by database FK constraints)
        self.repository.delete(id)

        return {
            "message": f"Superdomain '{superdomain.name}' deleted successfully",
            "affectedDomains": impact["affected_domains"],
            "affectedEntities": impact["affected_entities"],
            "cascade": impact["cascade"],
        }

    def _to_dict(self, superdomain) -> Dict:
        """Convert superdomain model to dictionary.

        Args:
            superdomain: Superdomain model instance

        Returns:
            Dictionary representation
        """
        return {
            "id": superdomain.id,
            "name": superdomain.name,
            "description": superdomain.description,
            "createdAt": superdomain.created_at.isoformat() if superdomain.created_at else None,
            "updatedAt": superdomain.updated_at.isoformat() if superdomain.updated_at else None,
            "createdBy": {
                "id": superdomain.creator.id,
                "username": superdomain.creator.username,
                "email": superdomain.creator.email,
            }
            if superdomain.creator
            else None,
        }
