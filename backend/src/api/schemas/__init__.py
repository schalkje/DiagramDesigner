"""Pydantic schemas for request/response validation."""
from .auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from .superdomain import (
    SuperdomainCreate,
    SuperdomainUpdate,
    SuperdomainResponse,
    SuperdomainListResponse,
)
from .domain import DomainCreate, DomainUpdate, DomainResponse, DomainListResponse
from .entity import EntityCreate, EntityUpdate, EntityResponse, EntityListResponse
from .attribute import AttributeCreate, AttributeUpdate, AttributeResponse, AttributeListResponse
from .relationship import RelationshipCreate, RelationshipResponse
from .diagram import (
    DiagramCreate,
    DiagramUpdate,
    DiagramResponse,
    DiagramObjectCreate,
    DiagramObjectUpdate,
    DiagramObjectResponse,
)

__all__ = [
    "LoginRequest",
    "LoginResponse",
    "RegisterRequest",
    "RegisterResponse",
    "SuperdomainCreate",
    "SuperdomainUpdate",
    "SuperdomainResponse",
    "SuperdomainListResponse",
    "DomainCreate",
    "DomainUpdate",
    "DomainResponse",
    "DomainListResponse",
    "EntityCreate",
    "EntityUpdate",
    "EntityResponse",
    "EntityListResponse",
    "AttributeCreate",
    "AttributeUpdate",
    "AttributeResponse",
    "AttributeListResponse",
    "RelationshipCreate",
    "RelationshipResponse",
    "DiagramCreate",
    "DiagramUpdate",
    "DiagramResponse",
    "DiagramObjectCreate",
    "DiagramObjectUpdate",
    "DiagramObjectResponse",
]
