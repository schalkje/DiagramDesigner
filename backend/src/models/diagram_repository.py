"""Diagram Repository models: Diagram, DiagramObject, DiagramRelationship."""
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from . import Base


class ObjectType(PyEnum):
    """Type of object that can be placed on a diagram."""

    SUPERDOMAIN = "SUPERDOMAIN"
    DOMAIN = "DOMAIN"
    ENTITY = "ENTITY"


class Diagram(Base):
    """Visual perspective on the data model with canvas settings."""

    __tablename__ = "diagram"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Core fields
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    purpose = Column(Text, nullable=True)

    # Extended fields (JSONB)
    tags = Column(JSONB, nullable=True)  # Array of tags for categorization
    canvas_settings = Column(JSONB, nullable=True)  # Zoom, pan, theme, grid settings

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # User tracking
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True, index=True)
    last_modified_by = Column(Integer, ForeignKey("user.id"), nullable=True)

    # Relationships
    objects = relationship(
        "DiagramObject",
        back_populates="diagram",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    diagram_relationships = relationship(
        "DiagramRelationship",
        back_populates="diagram",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_diagrams")
    last_modifier = relationship("User", foreign_keys=[last_modified_by])

    def __repr__(self) -> str:
        """String representation."""
        return f"<Diagram(id={self.id}, name='{self.name}')>"


class DiagramObject(Base):
    """Object (Superdomain, Domain, or Entity) placed on a specific diagram."""

    __tablename__ = "diagram_object"
    __table_args__ = (
        UniqueConstraint(
            "diagram_id", "object_type", "object_id", name="uq_diagram_object_unique"
        ),
    )

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    diagram_id = Column(
        Integer,
        ForeignKey("diagram.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Polymorphic reference to object
    object_type = Column(Enum(ObjectType, name="object_type_enum"), nullable=False)
    object_id = Column(Integer, nullable=False)

    # Position and size
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
    width = Column(Float, nullable=True)  # Null = auto
    height = Column(Float, nullable=True)  # Null = auto

    # Visual properties
    z_index = Column(Integer, nullable=False, default=0)
    visual_style = Column(JSONB, nullable=True)  # Custom styling overrides
    is_collapsed = Column(Boolean, nullable=False, default=False)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    diagram = relationship("Diagram", back_populates="objects")

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<DiagramObject(id={self.id}, diagram_id={self.diagram_id}, "
            f"type={self.object_type.value}, object_id={self.object_id}, "
            f"pos=({self.position_x}, {self.position_y}))>"
        )


class DiagramRelationship(Base):
    """Relationship line displayed on a specific diagram with visual routing."""

    __tablename__ = "diagram_relationship"
    __table_args__ = (
        UniqueConstraint(
            "diagram_id", "relationship_id", name="uq_diagram_relationship_unique"
        ),
    )

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    diagram_id = Column(
        Integer,
        ForeignKey("diagram.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    relationship_id = Column(
        Integer,
        ForeignKey("relationship.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Visibility
    is_visible = Column(Boolean, nullable=False, default=True)

    # Routing
    path_points = Column(JSONB, nullable=True)  # Custom routing points
    source_anchor = Column(String(20), nullable=True)  # top, bottom, left, right, auto
    target_anchor = Column(String(20), nullable=True)

    # Visual properties
    visual_style = Column(JSONB, nullable=True)  # Custom line styling

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    diagram = relationship("Diagram", back_populates="diagram_relationships")
    relationship_ref = relationship("Relationship")

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<DiagramRelationship(id={self.id}, diagram_id={self.diagram_id}, "
            f"relationship_id={self.relationship_id}, visible={self.is_visible})>"
        )
