"""Diagram service for business logic."""
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from ..repositories.diagram_repository import DiagramRepository


class DiagramService:
    """Service for Diagram business logic with object/relationship management."""

    def __init__(self, db: Session):
        """Initialize diagram service.

        Args:
            db: Database session
        """
        self.db = db
        self.repository = DiagramRepository(db)

    def get_by_id(self, id: int, include_details: bool = True) -> Optional[Dict]:
        """Get diagram by ID.

        Args:
            id: Diagram ID
            include_details: Whether to include objects and relationships

        Returns:
            Diagram dict or None
        """
        if include_details:
            diagram = self.repository.get_with_details(id)
        else:
            diagram = self.repository.get(id)

        if not diagram:
            return None

        return self._to_dict(diagram, include_details=include_details)

    def list(
        self,
        page: int = 1,
        page_size: int = 100,
        tag: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> Dict:
        """List diagrams with pagination and optional filtering.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            tag: Optional tag filter
            user_id: Optional user filter

        Returns:
            Dictionary with data and pagination info
        """
        skip = (page - 1) * page_size

        if tag:
            diagrams = self.repository.search_by_tag(tag, skip=skip, limit=page_size)
            total = len(self.repository.search_by_tag(tag, skip=0, limit=10000))
        elif user_id:
            diagrams = self.repository.get_by_user(user_id, skip=skip, limit=page_size)
            total = len(self.repository.get_by_user(user_id, skip=0, limit=10000))
        else:
            diagrams = self.repository.list(skip=skip, limit=page_size)
            total = self.repository.count()

        return {
            "data": [self._to_dict(d, include_details=False) for d in diagrams],
            "pagination": {
                "page": page,
                "pageSize": page_size,
                "total": total,
                "totalPages": (total + page_size - 1) // page_size,
            },
        }

    def create(self, data: Dict, user_id: Optional[int] = None) -> Dict:
        """Create new diagram.

        Args:
            data: Diagram data (name, description, purpose, tags)
            user_id: Creator user ID

        Returns:
            Created diagram dict

        Raises:
            ValueError: If validation fails
        """
        # Validation
        name = data.get("name", "").strip()
        if not name:
            raise ValueError("Diagram name is required")

        if len(name) > 100:
            raise ValueError("Diagram name must be 100 characters or less")

        # Create
        create_data = {
            "name": name,
            "description": data.get("description"),
            "purpose": data.get("purpose"),
            "tags": data.get("tags", []),
            "canvas_settings": data.get("canvasSettings"),
            "created_by": user_id,
            "last_modified_by": user_id,
        }

        diagram = self.repository.create(create_data)
        return self._to_dict(diagram, include_details=True)

    def update(self, id: int, data: Dict, user_id: Optional[int] = None) -> Optional[Dict]:
        """Update diagram metadata.

        Args:
            id: Diagram ID
            data: Fields to update
            user_id: User making the update

        Returns:
            Updated diagram dict or None

        Raises:
            ValueError: If validation fails
        """
        diagram = self.repository.get(id)
        if not diagram:
            return None

        # Validation
        if "name" in data:
            name = data["name"].strip()
            if not name:
                raise ValueError("Diagram name cannot be empty")

            if len(name) > 100:
                raise ValueError("Diagram name must be 100 characters or less")

        # Track last modifier
        if user_id:
            data["last_modified_by"] = user_id

        # Update
        updated = self.repository.update(id, data)
        return self._to_dict(updated, include_details=True) if updated else None

    def delete(self, id: int) -> Dict:
        """Delete diagram.

        Args:
            id: Diagram ID

        Returns:
            Success message

        Raises:
            ValueError: If diagram not found
        """
        diagram = self.repository.get(id)
        if not diagram:
            raise ValueError("Diagram not found")

        self.repository.delete(id)

        return {
            "message": f"Diagram '{diagram.name}' deleted successfully",
        }

    def add_object(self, diagram_id: int, object_data: Dict) -> Dict:
        """Add object to diagram.

        Args:
            diagram_id: Diagram ID
            object_data: Object data (objectType, objectId, positionX, positionY, etc.)

        Returns:
            Created diagram object dict

        Raises:
            ValueError: If validation fails
        """
        # Verify diagram exists
        diagram = self.repository.get(diagram_id)
        if not diagram:
            raise ValueError(f"Diagram with ID {diagram_id} not found")

        # Validation
        if "objectType" not in object_data:
            raise ValueError("Object type is required")

        if "objectId" not in object_data:
            raise ValueError("Object ID is required")

        if "positionX" not in object_data or "positionY" not in object_data:
            raise ValueError("Position (x, y) is required")

        # Create
        diagram_object = self.repository.add_object(diagram_id, object_data)

        return {
            "id": diagram_object.id,
            "diagramId": diagram_object.diagram_id,
            "objectType": diagram_object.object_type.value,
            "objectId": diagram_object.object_id,
            "positionX": diagram_object.position_x,
            "positionY": diagram_object.position_y,
        }

    def update_object_position(
        self, diagram_id: int, object_id: int, position_x: float, position_y: float
    ) -> Optional[Dict]:
        """Update object position on diagram.

        Args:
            diagram_id: Diagram ID
            object_id: DiagramObject ID
            position_x: New X coordinate
            position_y: New Y coordinate

        Returns:
            Updated object dict or None
        """
        updated = self.repository.update_object_position(object_id, position_x, position_y)
        if not updated:
            return None

        return {
            "id": updated.id,
            "positionX": updated.position_x,
            "positionY": updated.position_y,
        }

    def remove_object(self, diagram_id: int, object_id: int) -> Dict:
        """Remove object from diagram.

        Args:
            diagram_id: Diagram ID
            object_id: DiagramObject ID

        Returns:
            Success message

        Raises:
            ValueError: If object not found
        """
        success = self.repository.remove_object(object_id)
        if not success:
            raise ValueError("Diagram object not found")

        return {"message": "Object removed from diagram"}

    def _to_dict(self, diagram, include_details: bool = False) -> Dict:
        """Convert diagram model to dictionary.

        Args:
            diagram: Diagram model instance
            include_details: Whether to include objects and relationships

        Returns:
            Dictionary representation
        """
        result = {
            "id": diagram.id,
            "name": diagram.name,
            "description": diagram.description,
            "purpose": diagram.purpose,
            "tags": diagram.tags or [],
            "canvasSettings": diagram.canvas_settings,
            "createdAt": diagram.created_at.isoformat() if diagram.created_at else None,
            "updatedAt": diagram.updated_at.isoformat() if diagram.updated_at else None,
        }

        if include_details:
            result["objects"] = [
                {
                    "id": obj.id,
                    "objectType": obj.object_type.value,
                    "objectId": obj.object_id,
                    "positionX": obj.position_x,
                    "positionY": obj.position_y,
                    "width": obj.width,
                    "height": obj.height,
                    "zIndex": obj.z_index,
                    "visualStyle": obj.visual_style,
                    "isCollapsed": obj.is_collapsed,
                }
                for obj in (diagram.objects or [])
            ]

            result["relationships"] = [
                {
                    "id": rel.id,
                    "relationshipId": rel.relationship_id,
                    "isVisible": rel.is_visible,
                    "sourceAnchor": rel.source_anchor,
                    "targetAnchor": rel.target_anchor,
                    "visualStyle": rel.visual_style,
                }
                for rel in (diagram.diagram_relationships or [])
            ]

        return result
