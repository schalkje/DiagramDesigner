"""Object Repository models: Superdomain, Domain, Entity, Attribute."""
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from . import Base


class Superdomain(Base):
    """Top-level container in data model hierarchy."""

    __tablename__ = "superdomain"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Core fields
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # User tracking
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)

    # Relationships
    domains = relationship(
        "Domain",
        back_populates="superdomain",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    creator = relationship("User", back_populates="created_superdomains", foreign_keys=[created_by])

    def __repr__(self) -> str:
        """String representation."""
        return f"<Superdomain(id={self.id}, name='{self.name}')>"


class Domain(Base):
    """Mid-level grouping within a superdomain."""

    __tablename__ = "domain"
    __table_args__ = (
        UniqueConstraint("superdomain_id", "name", name="uq_domain_superdomain_name"),
    )

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    superdomain_id = Column(
        Integer, ForeignKey("superdomain.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Core fields
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # User tracking
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)

    # Relationships
    superdomain = relationship("Superdomain", back_populates="domains")
    entities = relationship(
        "Entity",
        back_populates="domain",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<Domain(id={self.id}, name='{self.name}', superdomain_id={self.superdomain_id})>"


class Entity(Base):
    """Business object or concept (equivalent to a database table)."""

    __tablename__ = "entity"
    __table_args__ = (UniqueConstraint("domain_id", "name", name="uq_entity_domain_name"),)

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    domain_id = Column(
        Integer, ForeignKey("domain.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Core fields
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # User tracking
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)

    # Relationships
    domain = relationship("Domain", back_populates="entities")
    attributes = relationship(
        "Attribute",
        back_populates="entity",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    relationships_from = relationship(
        "Relationship",
        foreign_keys="Relationship.source_entity_id",
        back_populates="source_entity",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    relationships_to = relationship(
        "Relationship",
        foreign_keys="Relationship.target_entity_id",
        back_populates="target_entity",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<Entity(id={self.id}, name='{self.name}', domain_id={self.domain_id})>"


class Attribute(Base):
    """Property or field of an entity (equivalent to a database column)."""

    __tablename__ = "attribute"
    __table_args__ = (UniqueConstraint("entity_id", "name", name="uq_attribute_entity_name"),)

    # Primary key (BIGINT for 100K+ attributes)
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Foreign keys
    entity_id = Column(
        Integer, ForeignKey("entity.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Core fields
    name = Column(String(100), nullable=False)
    data_type = Column(String(50), nullable=False)
    is_nullable = Column(Boolean, nullable=False, default=True)
    default_value = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    # Extended fields (JSONB)
    constraints = Column(JSONB, nullable=True)
    data_quality_rules = Column(JSONB, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # User tracking
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)

    # Relationships
    entity = relationship("Entity", back_populates="attributes")

    # Valid data types (from OpenAPI spec)
    VALID_DATA_TYPES = [
        "String",
        "Text",
        "Integer",
        "BigInteger",
        "Float",
        "Decimal",
        "Boolean",
        "Date",
        "DateTime",
        "Time",
        "UUID",
        "JSON",
    ]

    def validate_data_type(self) -> bool:
        """Validate that data_type is from allowed list."""
        return self.data_type in self.VALID_DATA_TYPES

    def __repr__(self) -> str:
        """String representation."""
        return f"<Attribute(id={self.id}, name='{self.name}', data_type='{self.data_type}', entity_id={self.entity_id})>"
