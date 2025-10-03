"""Entity request/response schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class EntityCreate(BaseModel):
    """Create entity request schema."""

    domain_id: int = Field(..., description="Parent domain ID")
    name: str = Field(..., min_length=1, max_length=100, description="Entity name")
    description: Optional[str] = Field(None, description="Entity description")


class EntityUpdate(BaseModel):
    """Update entity request schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Entity name")
    description: Optional[str] = Field(None, description="Entity description")


class EntityResponse(BaseModel):
    """Entity response schema."""

    id: int = Field(..., description="Entity ID")
    domain_id: int = Field(..., description="Parent domain ID")
    name: str = Field(..., description="Entity name")
    description: Optional[str] = Field(None, description="Entity description")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class EntityListResponse(BaseModel):
    """List of entities response schema."""

    entities: List[EntityResponse] = Field(..., description="List of entities")
    total: int = Field(..., description="Total count")
