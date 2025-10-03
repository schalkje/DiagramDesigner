"""Authentication request/response schemas."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")


class LoginResponse(BaseModel):
    """Login response schema."""

    token: str = Field(..., description="JWT authentication token")
    user: dict = Field(..., description="User information")


class RegisterRequest(BaseModel):
    """User registration request schema."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=8, description="User password")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")


class RegisterResponse(BaseModel):
    """User registration response schema."""

    token: str = Field(..., description="JWT authentication token")
    user: dict = Field(..., description="Created user information")
