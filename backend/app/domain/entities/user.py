from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class User(BaseModel):
    """User entity representing a system user"""

    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50,
                          description="Username")
    full_name: str = Field(..., min_length=1,
                           max_length=100, description="Full name")
    role: str = Field(default="user", description="User role")
    is_active: bool = Field(default=True, description="User active status")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Account creation date")

    @validator('username')
    def validate_username(cls, v):
        """Validate username format"""
        if not v.isalnum():
            raise ValueError(
                "Username must contain only alphanumeric characters")
        return v.lower()

    @validator('role')
    def validate_role(cls, v):
        """Validate user role"""
        valid_roles = ['user', 'analyst', 'admin']
        if v not in valid_roles:
            raise ValueError(f"Role must be one of: {valid_roles}")
        return v

    class Config:
        from_attributes = True


class UserRole:
    """User role constants"""

    USER = "user"
    ANALYST = "analyst"
    ADMIN = "admin"
