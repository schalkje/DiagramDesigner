"""Domain request/response schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DomainCreate(BaseModel):
    """Create domain request schema."""

    superdomain_id: int = Field(..., description="Parent superdomain ID")
    name: str = Field(..., min_length=1, max_length=100, description="Domain name")
    description: Optional[str] = Field(None, description="Domain description")


class DomainUpdate(BaseModel):
    """Update domain request schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Domain name")
    description: Optional[str] = Field(None, description="Domain description")


class DomainResponse(BaseModel):
    """Domain response schema."""

    id: int = Field(..., description="Domain ID")
    superdomain_id: int = Field(..., description="Parent superdomain ID")
    name: str = Field(..., description="Domain name")
    description: Optional[str] = Field(None, description="Domain description")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class DomainListResponse(BaseModel):
    """List of domains response schema."""

    domains: List[DomainResponse] = Field(..., description="List of domains")
    total: int = Field(..., description="Total count")
