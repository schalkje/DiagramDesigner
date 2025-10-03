"""Diagram request/response schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DiagramCreate(BaseModel):
    """Create diagram request schema."""

    name: str = Field(..., min_length=1, max_length=200, description="Diagram name")
    description: Optional[str] = Field(None, description="Diagram description")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")
    canvas_settings: Optional[dict] = Field(None, description="Canvas settings (JSON)")


class DiagramUpdate(BaseModel):
    """Update diagram request schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Diagram name")
    description: Optional[str] = Field(None, description="Diagram description")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")
    canvas_settings: Optional[dict] = Field(None, description="Canvas settings (JSON)")


class DiagramResponse(BaseModel):
    """Diagram response schema."""

    id: int = Field(..., description="Diagram ID")
    user_id: int = Field(..., description="Owner user ID")
    name: str = Field(..., description="Diagram name")
    description: Optional[str] = Field(None, description="Diagram description")
    tags: Optional[List[str]] = Field(None, description="Tags")
    canvas_settings: Optional[dict] = Field(None, description="Canvas settings")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class DiagramObjectCreate(BaseModel):
    """Add object to diagram request schema."""

    object_type: str = Field(..., description="Object type (SUPERDOMAIN, DOMAIN, ENTITY)")
    object_id: int = Field(..., description="Object ID (from object repository)")
    position_x: float = Field(..., description="X coordinate on canvas")
    position_y: float = Field(..., description="Y coordinate on canvas")
    visual_style: Optional[dict] = Field(None, description="Visual style overrides (JSON)")


class DiagramObjectUpdate(BaseModel):
    """Update diagram object request schema."""

    position_x: Optional[float] = Field(None, description="X coordinate on canvas")
    position_y: Optional[float] = Field(None, description="Y coordinate on canvas")
    visual_style: Optional[dict] = Field(None, description="Visual style overrides (JSON)")


class DiagramObjectResponse(BaseModel):
    """Diagram object response schema."""

    id: int = Field(..., description="Diagram object ID")
    diagram_id: int = Field(..., description="Parent diagram ID")
    object_type: str = Field(..., description="Object type")
    object_id: int = Field(..., description="Object ID from repository")
    position_x: float = Field(..., description="X coordinate")
    position_y: float = Field(..., description="Y coordinate")
    visual_style: Optional[dict] = Field(None, description="Visual style")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
