"""User model with authentication support."""
from datetime import datetime
from enum import Enum as PyEnum

import bcrypt
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class AuthProvider(PyEnum):
    """Authentication provider enum."""

    LOCAL = "LOCAL"
    AZURE_AD = "AZURE_AD"


class User(Base):
    """User model for authentication and authorization."""

    __tablename__ = "user"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Authentication fields
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=True)

    # Profile fields
    full_name = Column(String(200), nullable=True)

    # External authentication
    auth_provider = Column(
        Enum(AuthProvider, name="auth_provider_enum"),
        nullable=False,
        default=AuthProvider.LOCAL,
    )
    external_id = Column(String(255), nullable=True)

    # Status
    is_active = Column(Boolean, nullable=False, default=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    # Relationships (created objects)
    created_superdomains = relationship(
        "Superdomain", back_populates="creator", foreign_keys="Superdomain.created_by"
    )
    created_diagrams = relationship(
        "Diagram", back_populates="creator", foreign_keys="Diagram.created_by"
    )

    def set_password(self, password: str) -> None:
        """Hash and set the user's password.

        Args:
            password: Plain text password to hash
        """
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Verify a password against the stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            True if password matches, False otherwise
        """
        if not self.password_hash:
            return False

        password_bytes = password.encode("utf-8")
        hash_bytes = self.password_hash.encode("utf-8")

        return bcrypt.checkpw(password_bytes, hash_bytes)

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
