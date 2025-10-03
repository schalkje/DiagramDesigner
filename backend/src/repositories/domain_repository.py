"""Domain repository for data access."""
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.object_repository import Domain
from .base_repository import BaseRepository


class DomainRepository(BaseRepository[Domain]):
    """Repository for Domain entities with superdomain filtering."""

    def __init__(self, db: Session):
        """Initialize domain repository.

        Args:
            db: Database session
        """
        super().__init__(Domain, db)

    def get_by_superdomain(
        self, superdomain_id: int, skip: int = 0, limit: int = 100
    ) -> List[Domain]:
        """Get domains by superdomain ID.

        Args:
            superdomain_id: Parent superdomain ID
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            List of Domain instances
        """
        return (
            self.db.query(Domain)
            .filter(Domain.superdomain_id == superdomain_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_name_and_superdomain(
        self, name: str, superdomain_id: int
    ) -> Optional[Domain]:
        """Get domain by name within a superdomain.

        Used for checking unique constraint: (superdomain_id, name).

        Args:
            name: Domain name
            superdomain_id: Parent superdomain ID

        Returns:
            Domain instance or None
        """
        return (
            self.db.query(Domain)
            .filter(Domain.name == name, Domain.superdomain_id == superdomain_id)
            .first()
        )

    def count_by_superdomain(self, superdomain_id: int) -> int:
        """Count domains in a superdomain.

        Args:
            superdomain_id: Parent superdomain ID

        Returns:
            Count of domains
        """
        return self.db.query(Domain).filter(Domain.superdomain_id == superdomain_id).count()
