"""Superdomain request/response schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SuperdomainCreate(BaseModel):
    """Create superdomain request schema."""

    name: str = Field(..., min_length=1, max_length=100, description="Superdomain name")
    description: Optional[str] = Field(None, description="Superdomain description")


class SuperdomainUpdate(BaseModel):
    """Update superdomain request schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Superdomain name")
    description: Optional[str] = Field(None, description="Superdomain description")


class SuperdomainResponse(BaseModel):
    """Superdomain response schema."""

    id: int = Field(..., description="Superdomain ID")
    name: str = Field(..., description="Superdomain name")
    description: Optional[str] = Field(None, description="Superdomain description")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class SuperdomainListResponse(BaseModel):
    """List of superdomains response schema."""

    superdomains: List[SuperdomainResponse] = Field(..., description="List of superdomains")
    total: int = Field(..., description="Total count")
