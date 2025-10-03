"""Authentication service for business logic."""
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

import jwt
from sqlalchemy.orm import Session

from ..models.user import AuthProvider
from ..repositories.user_repository import UserRepository


class AuthService:
    """Service for authentication and authorization with JWT."""

    def __init__(self, db: Session):
        """Initialize auth service.

        Args:
            db: Database session
        """
        self.db = db
        self.repository = UserRepository(db)
        self.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.token_expiry_hours = 24

    def register(self, data: Dict) -> Dict:
        """Register a new user.

        Args:
            data: User data (email, username, password, fullName)

        Returns:
            Created user dict with token

        Raises:
            ValueError: If validation fails
        """
        # Validation
        email = data.get("email", "").strip().lower()
        if not email:
            raise ValueError("Email is required")

        if self.repository.email_exists(email):
            raise ValueError("Email already registered")

        username = data.get("username", "").strip()
        if not username:
            raise ValueError("Username is required")

        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")

        if self.repository.username_exists(username):
            raise ValueError("Username already taken")

        password = data.get("password", "")
        if not password:
            raise ValueError("Password is required")

        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")

        # Create user
        from ..models.user import User

        user = User(
            email=email,
            username=username,
            full_name=data.get("fullName"),
            auth_provider=AuthProvider.LOCAL,
            is_active=True,
        )
        user.set_password(password)

        # Save to database
        create_data = {
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
            "full_name": user.full_name,
            "auth_provider": user.auth_provider,
            "is_active": user.is_active,
        }

        created_user = self.repository.create(create_data)

        # Generate token
        token = self._generate_token(created_user.id, created_user.email)

        return {
            "token": token,
            "user": self._user_to_dict(created_user),
        }

    def login(self, email: str, password: str) -> Dict:
        """Authenticate user with email and password.

        Args:
            email: User email
            password: Plain text password

        Returns:
            Token and user dict

        Raises:
            ValueError: If authentication fails
        """
        email = email.strip().lower()

        user = self.repository.authenticate(email, password)
        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Account is deactivated")

        # Generate token
        token = self._generate_token(user.id, user.email)

        return {
            "token": token,
            "user": self._user_to_dict(user),
        }

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return user data.

        Args:
            token: JWT token

        Returns:
            User dict or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            user_id = payload.get("user_id")
            if not user_id:
                return None

            user = self.repository.get(user_id)
            if not user or not user.is_active:
                return None

            return self._user_to_dict(user)

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User dict or None
        """
        user = self.repository.get(user_id)
        if not user:
            return None

        return self._user_to_dict(user)

    def _generate_token(self, user_id: int, email: str) -> str:
        """Generate JWT token for user.

        Args:
            user_id: User ID
            email: User email

        Returns:
            JWT token string
        """
        expiry = datetime.utcnow() + timedelta(hours=self.token_expiry_hours)

        payload = {
            "user_id": user_id,
            "email": email,
            "exp": expiry,
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def _user_to_dict(self, user) -> Dict:
        """Convert user model to dictionary.

        Args:
            user: User model instance

        Returns:
            Dictionary representation (without sensitive fields)
        """
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "fullName": user.full_name,
            "createdAt": user.created_at.isoformat() if user.created_at else None,
        }
