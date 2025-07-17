import logging
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from ...infrastructure.repositories import InsightRepository
from ...infrastructure.database import get_db
from ..schemas import (
    InsightDetailResponse, InsightListResponse, InsightHealthResponse, InsightInfo
)

logger = logging.getLogger("insight_routes")

# Create router
router = APIRouter(prefix="/api/v1/insights", tags=["insights"])


@router.get(
    "/health",
    response_model=InsightHealthResponse,
    summary="Insight service health check",
    description="Check if the insight service is healthy"
)
async def insight_service_health():
    """
    Health check endpoint for insight service

    Returns:
        InsightHealthResponse with service health status
    """
    return InsightHealthResponse(
        service="insight_processing",
        status="healthy",
        message="Insight service is operational"
    )


@router.get(
    "/{insight_id}",
    response_model=InsightDetailResponse,
    summary="Get insight by ID",
    description="Retrieve a specific insight by its ID"
)
async def get_insight(insight_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an insight by its ID

    Args:
        insight_id: Insight ID
        db: Database session dependency

    Returns:
        InsightDetailResponse with insight information
    """
    try:
        logger.info(f"Retrieving insight by ID: {insight_id}")
        insight_repository = InsightRepository(db)
        insight = insight_repository.get_by_id(insight_id)

        if not insight:
            logger.warning(f"Insight not found: {insight_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insight not found"
            )

        return InsightDetailResponse(
            insight=InsightInfo(
                id=insight.id,
                query_id=insight.query_id,
                title=insight.title,
                description=insight.description,
                category=insight.category,
                confidence_score=insight.confidence_score,
                data_sources=insight.data_sources,
                created_at=insight.created_at.isoformat()
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error during insight retrieval: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the insight"
        )


@router.get(
    "/query/{query_id}",
    response_model=InsightListResponse,
    summary="Get insights by query ID",
    description="Retrieve all insights for a specific query"
)
async def get_insights_by_query(query_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all insights for a specific query

    Args:
        query_id: Query ID
        db: Database session dependency

    Returns:
        InsightListResponse with list of insights for the query
    """
    try:
        insight_repository = InsightRepository(db)
        insights = insight_repository.get_by_query_id(query_id)

        insight_list = [
            InsightInfo(
                id=insight.id,
                query_id=insight.query_id,
                title=insight.title,
                description=insight.description,
                category=insight.category,
                confidence_score=insight.confidence_score,
                data_sources=insight.data_sources,
                created_at=insight.created_at.isoformat()
            )
            for insight in insights
        ]

        return InsightListResponse(
            insights=insight_list,
            count=len(insight_list)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving insights"
        )


@router.get(
    "/category/{category}",
    response_model=InsightListResponse,
    summary="Get insights by category",
    description="Retrieve all insights for a specific category"
)
async def get_insights_by_category(category: str, db: Session = Depends(get_db)):
    """
    Retrieve all insights for a specific category

    Args:
        category: Insight category
        db: Database session dependency

    Returns:
        InsightListResponse with list of insights for the category
    """
    try:
        insight_repository = InsightRepository(db)
        insights = insight_repository.get_by_category(category)

        insight_list = [
            InsightInfo(
                id=insight.id,
                query_id=insight.query_id,
                title=insight.title,
                description=insight.description,
                category=insight.category,
                confidence_score=insight.confidence_score,
                data_sources=insight.data_sources,
                created_at=insight.created_at.isoformat()
            )
            for insight in insights
        ]

        return InsightListResponse(
            insights=insight_list,
            count=len(insight_list)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving insights"
        )
