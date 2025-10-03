"""Superdomain repository for data access."""
from typing import Dict, List

from sqlalchemy.orm import Session

from ..models.object_repository import Domain, Entity, Superdomain
from .base_repository import BaseRepository


class SuperdomainRepository(BaseRepository[Superdomain]):
    """Repository for Superdomain entities with cascade delete analysis."""

    def __init__(self, db: Session):
        """Initialize superdomain repository.

        Args:
            db: Database session
        """
        super().__init__(Superdomain, db)

    def get_by_name(self, name: str) -> Superdomain | None:
        """Get superdomain by name.

        Args:
            name: Superdomain name

        Returns:
            Superdomain instance or None
        """
        return self.db.query(Superdomain).filter(Superdomain.name == name).first()

    def analyze_delete_impact(self, id: int) -> Dict[str, any]:
        """Analyze the impact of deleting a superdomain.

        Args:
            id: Superdomain ID

        Returns:
            Dictionary with impact details:
            - affected_domains: List of domain names
            - affected_entities: List of entity names
            - total_domains: Count of domains
            - total_entities: Count of entities
            - cascade: True if cascade delete will occur
        """
        superdomain = self.get(id)
        if not superdomain:
            return {
                "affected_domains": [],
                "affected_entities": [],
                "total_domains": 0,
                "total_entities": 0,
                "cascade": False,
            }

        # Get affected domains
        domains = self.db.query(Domain).filter(Domain.superdomain_id == id).all()

        # Get affected entities (through domains)
        domain_ids = [d.id for d in domains]
        entities = (
            self.db.query(Entity).filter(Entity.domain_id.in_(domain_ids)).all()
            if domain_ids
            else []
        )

        return {
            "affected_domains": [d.name for d in domains],
            "affected_entities": [e.name for e in entities],
            "total_domains": len(domains),
            "total_entities": len(entities),
            "cascade": len(domains) > 0 or len(entities) > 0,
        }

    def list_with_counts(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """List superdomains with domain counts.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            List of dictionaries with superdomain and domain_count
        """
        from sqlalchemy import func

        results = (
            self.db.query(Superdomain, func.count(Domain.id).label("domain_count"))
            .outerjoin(Domain)
            .group_by(Superdomain.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [
            {
                "superdomain": superdomain,
                "domain_count": domain_count,
            }
            for superdomain, domain_count in results
        ]
