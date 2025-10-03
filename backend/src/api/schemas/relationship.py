"""Relationship request/response schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RelationshipCreate(BaseModel):
    """Create relationship request schema."""

    source_entity_id: int = Field(..., description="Source entity ID")
    target_entity_id: int = Field(..., description="Target entity ID")
    source_role: str = Field(..., min_length=1, max_length=100, description="Source role name")
    target_role: str = Field(..., min_length=1, max_length=100, description="Target role name")
    source_cardinality: str = Field(
        ..., description="Source cardinality (ZERO_ONE, ONE, ZERO_MANY, ONE_MANY)"
    )
    target_cardinality: str = Field(
        ..., description="Target cardinality (ZERO_ONE, ONE, ZERO_MANY, ONE_MANY)"
    )
    description: Optional[str] = Field(None, description="Relationship description")


class RelationshipResponse(BaseModel):
    """Relationship response schema."""

    id: int = Field(..., description="Relationship ID")
    source_entity_id: int = Field(..., description="Source entity ID")
    target_entity_id: int = Field(..., description="Target entity ID")
    source_role: str = Field(..., description="Source role name")
    target_role: str = Field(..., description="Target role name")
    source_cardinality: str = Field(..., description="Source cardinality")
    target_cardinality: str = Field(..., description="Target cardinality")
    description: Optional[str] = Field(None, description="Relationship description")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
