import logging
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Union
from ..schemas import (
    QueryRequest, QueryResponse, QueryDetailResponse,
    QueryHealthResponse, ErrorResponse
)
from ...application.use_cases import ProcessQueryUseCase
from ...domain.services import QueryProcessingService
from ...infrastructure.repositories import QueryRepository, InsightRepository
from ...infrastructure.database import get_db

logger = logging.getLogger("query_routes")

# Create router
router = APIRouter(prefix="/api/v1/queries", tags=["queries"])


@router.post(
    "/process",
    response_model=Union[QueryResponse, ErrorResponse],
    status_code=status.HTTP_200_OK,
    summary="Process natural language query",
    description="Process a natural language query and return AI-generated insights"
)
async def process_query(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Process a natural language query and generate insights

    Args:
        request: QueryRequest containing the natural language query
        db: Database session dependency

    Returns:
        QueryResponse with insights and recommendations, or ErrorResponse if processing fails
    """
    try:
        logger.info(f"Processing query: {request.query_text}", extra={
                    "user_id": request.user_id})
        # Initialize services and use cases with dependencies
        query_processing_service = QueryProcessingService()
        query_repository = QueryRepository(db)
        insight_repository = InsightRepository(db)
        process_query_use_case = ProcessQueryUseCase(
            query_processing_service, query_repository, insight_repository)

        # Execute the use case
        result = await process_query_use_case.execute(
            query_text=request.query_text,
            user_id=request.user_id
        )

        # Check if processing was successful
        if result["success"]:
            logger.info(f"Query processed successfully", extra={
                        "user_id": request.user_id, "query": result["query"]})
            return QueryResponse(**result)
        else:
            logger.warning(f"Query processing failed: {result['message']}", extra={
                           "user_id": request.user_id})
            # Return error response with appropriate status code
            if result["error"] == "Validation error":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["message"]
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result["message"]
                )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error during query processing: {str(e)}", exc_info=True)
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the query"
        )


@router.get(
    "/health",
    response_model=QueryHealthResponse,
    summary="Query service health check",
    description="Check if the query processing service is healthy"
)
async def query_service_health():
    """
    Health check endpoint for query processing service

    Returns:
        QueryHealthResponse with service health status
    """
    return QueryHealthResponse(
        service="query_processing",
        status="healthy",
        message="Query processing service is operational"
    )


@router.get(
    "/{query_id}",
    response_model=QueryDetailResponse,
    summary="Get query by ID",
    description="Retrieve a specific query by its ID"
)
async def get_query(query_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a query by its ID

    Args:
        query_id: Query ID
        db: Database session dependency

    Returns:
        QueryDetailResponse with query information
    """
    try:
        query_repository = QueryRepository(db)
        query = query_repository.get_by_id(query_id)

        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Query not found"
            )

        return QueryDetailResponse(
            query={
                "id": query.id,
                "text": query.text,
                "user_id": query.user_id,
                "processed": query.processed,
                "response": query.response,
                "created_at": query.created_at.isoformat()
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the query"
        )
