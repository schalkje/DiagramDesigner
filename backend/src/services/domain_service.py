"""Domain service for business logic."""
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from ..repositories.domain_repository import DomainRepository
from ..repositories.superdomain_repository import SuperdomainRepository


class DomainService:
    """Service for Domain business logic with validation."""

    def __init__(self, db: Session):
        """Initialize domain service.

        Args:
            db: Database session
        """
        self.db = db
        self.repository = DomainRepository(db)
        self.superdomain_repository = SuperdomainRepository(db)

    def get_by_id(self, id: int) -> Optional[Dict]:
        """Get domain by ID.

        Args:
            id: Domain ID

        Returns:
            Domain dict or None
        """
        domain = self.repository.get(id)
        if not domain:
            return None

        return self._to_dict(domain)

    def list(
        self,
        page: int = 1,
        page_size: int = 100,
        superdomain_id: Optional[int] = None,
    ) -> Dict:
        """List domains with pagination and optional filtering.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            superdomain_id: Optional superdomain filter

        Returns:
            Dictionary with data and pagination info
        """
        skip = (page - 1) * page_size

        if superdomain_id:
            domains = self.repository.get_by_superdomain(
                superdomain_id, skip=skip, limit=page_size
            )
            total = self.repository.count_by_superdomain(superdomain_id)
        else:
            domains = self.repository.list(skip=skip, limit=page_size)
            total = self.repository.count()

        return {
            "data": [self._to_dict(d) for d in domains],
            "pagination": {
                "page": page,
                "pageSize": page_size,
                "total": total,
                "totalPages": (total + page_size - 1) // page_size,
            },
        }

    def create(self, data: Dict, user_id: Optional[int] = None) -> Dict:
        """Create new domain.

        Args:
            data: Domain data (superdomainId, name, description)
            user_id: Creator user ID

        Returns:
            Created domain dict

        Raises:
            ValueError: If validation fails
        """
        # Validation
        superdomain_id = data.get("superdomainId")
        if not superdomain_id:
            raise ValueError("Superdomain ID is required")

        # Verify superdomain exists
        superdomain = self.superdomain_repository.get(superdomain_id)
        if not superdomain:
            raise ValueError(f"Superdomain with ID {superdomain_id} not found")

        name = data.get("name", "").strip()
        if not name:
            raise ValueError("Domain name is required")

        if len(name) > 100:
            raise ValueError("Domain name must be 100 characters or less")

        # Check unique constraint: (superdomain_id, name)
        existing = self.repository.get_by_name_and_superdomain(name, superdomain_id)
        if existing:
            raise ValueError(
                f"Domain with name '{name}' already exists in superdomain '{superdomain.name}'"
            )

        # Create
        create_data = {
            "superdomain_id": superdomain_id,
            "name": name,
            "description": data.get("description"),
            "created_by": user_id,
        }

        domain = self.repository.create(create_data)
        return self._to_dict(domain)

    def update(self, id: int, data: Dict) -> Optional[Dict]:
        """Update domain.

        Args:
            id: Domain ID
            data: Fields to update

        Returns:
            Updated domain dict or None

        Raises:
            ValueError: If validation fails
        """
        domain = self.repository.get(id)
        if not domain:
            return None

        # Validation
        if "name" in data:
            name = data["name"].strip()
            if not name:
                raise ValueError("Domain name cannot be empty")

            if len(name) > 100:
                raise ValueError("Domain name must be 100 characters or less")

            # Check unique constraint (excluding current domain)
            existing = self.repository.get_by_name_and_superdomain(
                name, domain.superdomain_id
            )
            if existing and existing.id != id:
                raise ValueError(
                    f"Domain with name '{name}' already exists in this superdomain"
                )

        # Update
        updated = self.repository.update(id, data)
        return self._to_dict(updated) if updated else None

    def delete(self, id: int) -> Dict:
        """Delete domain.

        Args:
            id: Domain ID

        Returns:
            Delete impact report

        Raises:
            ValueError: If domain not found
        """
        domain = self.repository.get(id)
        if not domain:
            raise ValueError("Domain not found")

        # Could add cascade impact analysis like SuperdomainService
        # For now, rely on database CASCADE DELETE

        self.repository.delete(id)

        return {
            "message": f"Domain '{domain.name}' deleted successfully",
            "cascade": True,  # Entities and attributes cascade deleted
        }

    def _to_dict(self, domain) -> Dict:
        """Convert domain model to dictionary.

        Args:
            domain: Domain model instance

        Returns:
            Dictionary representation
        """
        return {
            "id": domain.id,
            "superdomainId": domain.superdomain_id,
            "name": domain.name,
            "description": domain.description,
            "createdAt": domain.created_at.isoformat() if domain.created_at else None,
            "updatedAt": domain.updated_at.isoformat() if domain.updated_at else None,
        }
