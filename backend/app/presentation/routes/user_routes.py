import logging
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from ...infrastructure.repositories import UserRepository
from ...infrastructure.database import get_db
from ...domain.entities.user import User
from ..schemas import (
    UserCreateRequest, UserCreateResponse, UserDetailResponse,
    UserListResponse, UserHealthResponse, UserInfo
)

logger = logging.getLogger("user_routes")

# Create router
router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get(
    "/health",
    response_model=UserHealthResponse,
    summary="User service health check",
    description="Check if the user service is healthy"
)
async def user_service_health():
    """
    Health check endpoint for user service

    Returns:
        UserHealthResponse with service health status
    """
    return UserHealthResponse(
        service="user_management",
        status="healthy",
        message="User service is operational"
    )


@router.post(
    "/",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
    description="Create a new user"
)
async def create_user(user_request: UserCreateRequest, db: Session = Depends(get_db)):
    """
    Create a new user

    Args:
        user_request: UserCreateRequest containing user information
        db: Database session dependency

    Returns:
        UserCreateResponse with created user information
    """
    try:
        logger.info(f"Creating user: {user_request.username}")
        user_repository = UserRepository(db)

        # Check if username already exists
        if user_repository.get_by_username(user_request.username):
            logger.warning(f"Username already exists: {user_request.username}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )

        # Create user entity from request
        user = User(
            username=user_request.username,
            full_name=user_request.full_name,
            role=user_request.role
        )

        user = user_repository.create(user)
        logger.info(f"User created successfully: {user.username}", extra={
                    "user_id": user.id})

        return UserCreateResponse(
            user=UserInfo(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at.isoformat()
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error during user creation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        )


@router.get(
    "/",
    response_model=UserListResponse,
    summary="List active users",
    description="Retrieve all active users"
)
async def list_active_users(db: Session = Depends(get_db)):
    """
    Retrieve all active users

    Args:
        db: Database session dependency

    Returns:
        UserListResponse with list of active users
    """
    try:
        user_repository = UserRepository(db)
        users = user_repository.list_active_users()

        user_list = [
            UserInfo(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at.isoformat()
            )
            for user in users
        ]

        return UserListResponse(
            users=user_list,
            count=len(user_list)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving users"
        )


@router.get(
    "/username/{username}",
    response_model=UserDetailResponse,
    summary="Get user by username",
    description="Retrieve a specific user by their username"
)
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Retrieve a user by their username

    Args:
        username: Username
        db: Database session dependency

    Returns:
        UserDetailResponse with user information
    """
    try:
        user_repository = UserRepository(db)
        user = user_repository.get_by_username(username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserDetailResponse(
            user=UserInfo(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at.isoformat()
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the user"
        )


@router.get(
    "/{user_id}",
    response_model=UserDetailResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID"
)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID

    Args:
        user_id: User ID
        db: Database session dependency

    Returns:
        UserDetailResponse with user information
    """
    try:
        user_repository = UserRepository(db)
        user = user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserDetailResponse(
            user=UserInfo(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at.isoformat()
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the user"
        )
