"""Attribute request/response schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AttributeCreate(BaseModel):
    """Create attribute request schema."""

    entity_id: int = Field(..., description="Parent entity ID")
    name: str = Field(..., min_length=1, max_length=100, description="Attribute name")
    data_type: str = Field(..., description="Data type (String, Integer, UUID, etc.)")
    is_nullable: bool = Field(False, description="Whether attribute can be null")
    is_primary_key: bool = Field(False, description="Whether attribute is primary key")
    default_value: Optional[str] = Field(None, description="Default value")
    constraints: Optional[dict] = Field(None, description="Additional constraints (JSON)")


class AttributeUpdate(BaseModel):
    """Update attribute request schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Attribute name")
    data_type: Optional[str] = Field(None, description="Data type")
    is_nullable: Optional[bool] = Field(None, description="Whether attribute can be null")
    is_primary_key: Optional[bool] = Field(None, description="Whether attribute is primary key")
    default_value: Optional[str] = Field(None, description="Default value")
    constraints: Optional[dict] = Field(None, description="Additional constraints (JSON)")


class AttributeResponse(BaseModel):
    """Attribute response schema."""

    id: int = Field(..., description="Attribute ID")
    entity_id: int = Field(..., description="Parent entity ID")
    name: str = Field(..., description="Attribute name")
    data_type: str = Field(..., description="Data type")
    is_nullable: bool = Field(..., description="Whether attribute can be null")
    is_primary_key: bool = Field(..., description="Whether attribute is primary key")
    default_value: Optional[str] = Field(None, description="Default value")
    constraints: Optional[dict] = Field(None, description="Additional constraints")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class AttributeListResponse(BaseModel):
    """List of attributes response schema."""

    attributes: List[AttributeResponse] = Field(..., description="List of attributes")
    total: int = Field(..., description="Total count")
