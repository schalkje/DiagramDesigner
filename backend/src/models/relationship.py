"""Relationship model for entity connections."""
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from . import Base


class Cardinality(PyEnum):
    """Cardinality enum for relationship endpoints."""

    ZERO_ONE = "ZERO_ONE"  # 0..1 (optional, at most one)
    ONE = "ONE"  # 1..1 (exactly one)
    ZERO_MANY = "ZERO_MANY"  # 0..N (optional, many)
    ONE_MANY = "ONE_MANY"  # 1..N (at least one, many)


class Relationship(Base):
    """Connection between two entities with cardinality configuration."""

    __tablename__ = "relationship"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys - Entities
    source_entity_id = Column(
        Integer,
        ForeignKey("entity.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_entity_id = Column(
        Integer,
        ForeignKey("entity.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Foreign keys - Attributes (optional, for FK-based relationships)
    source_attribute_id = Column(BigInteger, ForeignKey("attribute.id"), nullable=True)
    target_attribute_id = Column(BigInteger, ForeignKey("attribute.id"), nullable=True)

    # Core fields
    name = Column(String(100), nullable=True)
    source_role = Column(String(100), nullable=True)
    target_role = Column(String(100), nullable=True)

    # Cardinality
    source_cardinality = Column(
        Enum(Cardinality, name="cardinality_enum"),
        nullable=False,
    )
    target_cardinality = Column(
        Enum(Cardinality, name="cardinality_enum"),
        nullable=False,
    )

    # Description
    description = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # User tracking
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)

    # Relationships
    source_entity = relationship(
        "Entity",
        foreign_keys=[source_entity_id],
        back_populates="relationships_from",
    )
    target_entity = relationship(
        "Entity",
        foreign_keys=[target_entity_id],
        back_populates="relationships_to",
    )

    def is_self_referential(self) -> bool:
        """Check if relationship is self-referential (source == target)."""
        return self.source_entity_id == self.target_entity_id

    def get_cardinality_notation(self) -> str:
        """Get human-readable cardinality notation (e.g., '1:N', '1:1', 'N:N')."""
        source_symbol = self._cardinality_to_symbol(self.source_cardinality)
        target_symbol = self._cardinality_to_symbol(self.target_cardinality)
        return f"{source_symbol}:{target_symbol}"

    @staticmethod
    def _cardinality_to_symbol(cardinality: Cardinality) -> str:
        """Convert cardinality enum to notation symbol."""
        if cardinality in (Cardinality.ZERO_ONE, Cardinality.ONE):
            return "1"
        else:  # ZERO_MANY, ONE_MANY
            return "N"

    def __repr__(self) -> str:
        """String representation."""
        notation = self.get_cardinality_notation()
        return (
            f"<Relationship(id={self.id}, "
            f"source_entity_id={self.source_entity_id}, "
            f"target_entity_id={self.target_entity_id}, "
            f"cardinality='{notation}')>"
        )
