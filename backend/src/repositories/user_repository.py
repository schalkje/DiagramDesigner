"""User repository for data access."""
from typing import Optional

from sqlalchemy.orm import Session

from ..models.user import User
from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User entities with authentication support."""

    def __init__(self, db: Session):
        """Initialize user repository.

        Args:
            db: Database session
        """
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address.

        Args:
            email: User email

        Returns:
            User instance or None
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username.

        Args:
            username: Username

        Returns:
            User instance or None
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_by_external_id(
        self, external_id: str, auth_provider: str
    ) -> Optional[User]:
        """Get user by external authentication provider ID.

        Args:
            external_id: External provider user ID
            auth_provider: Authentication provider name

        Returns:
            User instance or None
        """
        return (
            self.db.query(User)
            .filter(
                User.external_id == external_id,
                User.auth_provider == auth_provider,
            )
            .first()
        )

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password.

        Args:
            email: User email
            password: Plain text password

        Returns:
            User instance if authenticated, None otherwise
        """
        user = self.get_by_email(email)
        if not user:
            return None

        if not user.check_password(password):
            return None

        # Update last login timestamp
        from datetime import datetime

        user.last_login_at = datetime.utcnow()
        self.db.commit()

        return user

    def email_exists(self, email: str) -> bool:
        """Check if email is already registered.

        Args:
            email: Email to check

        Returns:
            True if exists, False otherwise
        """
        return self.db.query(User.id).filter(User.email == email).first() is not None

    def username_exists(self, username: str) -> bool:
        """Check if username is already taken.

        Args:
            username: Username to check

        Returns:
            True if exists, False otherwise
        """
        return (
            self.db.query(User.id).filter(User.username == username).first() is not None
        )

    def get_active_users(self, skip: int = 0, limit: int = 100):
        """Get active users.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            List of active User instances
        """
        return (
            self.db.query(User)
            .filter(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def deactivate_user(self, id: int) -> bool:
        """Deactivate a user (soft delete).

        Args:
            id: User ID

        Returns:
            True if deactivated, False if not found
        """
        user = self.get(id)
        if not user:
            return False

        user.is_active = False
        self.db.commit()
        return True

    def activate_user(self, id: int) -> bool:
        """Reactivate a user.

        Args:
            id: User ID

        Returns:
            True if activated, False if not found
        """
        user = self.get(id)
        if not user:
            return False

        user.is_active = True
        self.db.commit()
        return True
