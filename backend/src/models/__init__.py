"""SQLAlchemy models for DiagramDesigner."""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models to ensure they're registered with SQLAlchemy
from .user import User
from .object_repository import Superdomain, Domain, Entity, Attribute
from .relationship import Relationship
from .diagram_repository import Diagram, DiagramObject, DiagramRelationship

__all__ = [
    'Base',
    'User',
    'Superdomain',
    'Domain',
    'Entity',
    'Attribute',
    'Relationship',
    'Diagram',
    'DiagramObject',
    'DiagramRelationship',
]
