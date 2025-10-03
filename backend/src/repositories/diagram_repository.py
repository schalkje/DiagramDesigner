"""Diagram repository for data access."""
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from ..models.diagram_repository import Diagram, DiagramObject, DiagramRelationship
from .base_repository import BaseRepository


class DiagramRepository(BaseRepository[Diagram]):
    """Repository for Diagram entities with full object and relationship loading."""

    def __init__(self, db: Session):
        """Initialize diagram repository.

        Args:
            db: Database session
        """
        super().__init__(Diagram, db)

    def get_with_details(self, id: int) -> Optional[Diagram]:
        """Get diagram by ID with all objects and relationships eagerly loaded.

        Args:
            id: Diagram ID

        Returns:
            Diagram instance with objects and relationships or None
        """
        return (
            self.db.query(Diagram)
            .options(
                joinedload(Diagram.objects),
                joinedload(Diagram.diagram_relationships),
            )
            .filter(Diagram.id == id)
            .first()
        )

    def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Diagram]:
        """Get diagrams created by a user.

        Args:
            user_id: Creator user ID
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            List of Diagram instances
        """
        return (
            self.db.query(Diagram)
            .filter(Diagram.created_by == user_id)
            .order_by(Diagram.updated_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_tag(self, tag: str, skip: int = 0, limit: int = 100) -> List[Diagram]:
        """Search diagrams by tag.

        Args:
            tag: Tag to search for
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            List of Diagram instances with matching tag
        """
        # PostgreSQL JSONB containment operator
        return (
            self.db.query(Diagram)
            .filter(Diagram.tags.contains([tag]))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def add_object(self, diagram_id: int, object_data: dict) -> DiagramObject:
        """Add an object to a diagram.

        Args:
            diagram_id: Diagram ID
            object_data: Dictionary with object_type, object_id, position_x, position_y, etc.

        Returns:
            Created DiagramObject instance
        """
        object_data["diagram_id"] = diagram_id
        diagram_object = DiagramObject(**object_data)
        self.db.add(diagram_object)
        self.db.commit()
        self.db.refresh(diagram_object)
        return diagram_object

    def update_object_position(
        self, object_id: int, position_x: float, position_y: float
    ) -> Optional[DiagramObject]:
        """Update object position on diagram.

        Args:
            object_id: DiagramObject ID
            position_x: New X coordinate
            position_y: New Y coordinate

        Returns:
            Updated DiagramObject or None
        """
        diagram_object = (
            self.db.query(DiagramObject).filter(DiagramObject.id == object_id).first()
        )
        if not diagram_object:
            return None

        diagram_object.position_x = position_x
        diagram_object.position_y = position_y
        self.db.commit()
        self.db.refresh(diagram_object)
        return diagram_object

    def remove_object(self, object_id: int) -> bool:
        """Remove object from diagram.

        Args:
            object_id: DiagramObject ID

        Returns:
            True if removed, False if not found
        """
        diagram_object = (
            self.db.query(DiagramObject).filter(DiagramObject.id == object_id).first()
        )
        if not diagram_object:
            return False

        self.db.delete(diagram_object)
        self.db.commit()
        return True

    def get_objects_by_diagram(self, diagram_id: int) -> List[DiagramObject]:
        """Get all objects in a diagram.

        Args:
            diagram_id: Diagram ID

        Returns:
            List of DiagramObject instances
        """
        return (
            self.db.query(DiagramObject)
            .filter(DiagramObject.diagram_id == diagram_id)
            .order_by(DiagramObject.z_index)
            .all()
        )

    def get_relationships_by_diagram(
        self, diagram_id: int
    ) -> List[DiagramRelationship]:
        """Get all relationships in a diagram.

        Args:
            diagram_id: Diagram ID

        Returns:
            List of DiagramRelationship instances
        """
        return (
            self.db.query(DiagramRelationship)
            .filter(DiagramRelationship.diagram_id == diagram_id)
            .all()
        )

    def get_diagrams_containing_object(
        self, object_type: str, object_id: int
    ) -> List[Diagram]:
        """Get all diagrams that contain a specific object.

        Args:
            object_type: Object type (SUPERDOMAIN, DOMAIN, ENTITY)
            object_id: Object ID

        Returns:
            List of Diagram instances
        """
        return (
            self.db.query(Diagram)
            .join(DiagramObject)
            .filter(
                DiagramObject.object_type == object_type,
                DiagramObject.object_id == object_id,
            )
            .all()
        )
