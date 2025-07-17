from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class UserCreateRequest(BaseModel):
    """Schema for user creation request"""

    username: str = Field(..., min_length=3, max_length=50,
                          description="Username")
    full_name: str = Field(..., min_length=1,
                           max_length=100, description="Full name")
    role: str = Field(..., description="User role")

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "full_name": "John Doe",
                "role": "analyst"
            }
        }


class UserInfo(BaseModel):
    """Schema for user information in responses"""

    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="Full name")
    role: str = Field(..., description="User role")
    is_active: bool = Field(..., description="Active status")
    created_at: str = Field(..., description="Creation timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "full_name": "John Doe",
                "role": "analyst",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00"
            }
        }


class UserCreateResponse(BaseModel):
    """Schema for user creation response"""

    user: UserInfo = Field(..., description="Created user information")

    class Config:
        schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "username": "john_doe",
                    "full_name": "John Doe",
                    "role": "analyst",
                    "is_active": True,
                    "created_at": "2024-01-15T10:30:00"
                }
            }
        }


class UserDetailResponse(BaseModel):
    """Schema for user detail response (GET by ID)"""

    user: UserInfo = Field(..., description="User information")

    class Config:
        schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "username": "john_doe",
                    "full_name": "John Doe",
                    "role": "analyst",
                    "is_active": True,
                    "created_at": "2024-01-15T10:30:00"
                }
            }
        }


class UserListResponse(BaseModel):
    """Schema for list of users response"""

    users: List[UserInfo] = Field(..., description="List of users")
    count: int = Field(..., description="Total number of users")

    class Config:
        schema_extra = {
            "example": {
                "users": [
                    {
                        "id": 1,
                        "username": "john_doe",
                        "full_name": "John Doe",
                        "role": "analyst",
                        "is_active": True,
                        "created_at": "2024-01-15T10:30:00"
                    }
                ],
                "count": 1
            }
        }


class HealthResponse(BaseModel):
    """Schema for health check responses"""

    service: str = Field(..., description="Service name")
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")

    class Config:
        schema_extra = {
            "example": {
                "service": "user_management",
                "status": "healthy",
                "message": "User service is operational"
            }
        }
