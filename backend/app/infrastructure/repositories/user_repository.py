from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.user import User as UserModel
from ...domain.entities.user import User
from datetime import datetime


class UserRepository:
    """
    Repository for managing User persistence.
    Provides CRUD operations for User objects.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with SQLAlchemy session.
        Args:
            db: SQLAlchemy session
        """
        self.db = db

    def create(self, user: User) -> User:
        """
        Persist a new User to the database.
        Args:
            user: User domain entity
        Returns:
            User domain entity with ID
        """
        db_user = UserModel(
            username=user.username,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at or datetime.utcnow()
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        user.id = db_user.id
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a User by its ID.
        Args:
            user_id: User ID
        Returns:
            User domain entity or None
        """
        db_user = self.db.query(UserModel).filter(
            UserModel.id == user_id).first()
        if db_user:
            return User(
                id=db_user.id,
                username=db_user.username,
                full_name=db_user.full_name,
                role=db_user.role,
                is_active=db_user.is_active,
                created_at=db_user.created_at
            )
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a User by username.
        Args:
            username: Username
        Returns:
            User domain entity or None
        """
        db_user = self.db.query(UserModel).filter(
            UserModel.username == username).first()
        if db_user:
            return User(
                id=db_user.id,
                username=db_user.username,
                full_name=db_user.full_name,
                role=db_user.role,
                is_active=db_user.is_active,
                created_at=db_user.created_at
            )
        return None

    def list_active_users(self) -> List[User]:
        """
        Retrieve all active users.
        Returns:
            List of active User domain entities
        """
        db_users = self.db.query(UserModel).filter(
            UserModel.is_active == True).all()
        return [
            User(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at
            ) for user in db_users
        ]

    def update(self, user: User) -> User:
        """
        Update an existing User in the database.
        Args:
            user: User domain entity
        Returns:
            Updated User domain entity
        """
        db_user = self.db.query(UserModel).filter(
            UserModel.id == user.id).first()
        if not db_user:
            raise ValueError("User not found")

        db_user.username = user.username
        db_user.full_name = user.full_name
        db_user.role = user.role
        db_user.is_active = user.is_active

        self.db.commit()
        self.db.refresh(db_user)
        return user
