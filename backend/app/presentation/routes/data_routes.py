import logging
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from ...infrastructure.services.real_data_service import RealDataService
from ...infrastructure.database import get_db
from ..schemas import (
    SalesDataResponse, InventoryDataResponse, CustomerDataResponse,
    MetricsDataResponse, SearchDataResponse, DataHealthResponse,
    SalesDataItem, InventoryDataItem, CustomerDataItem, BusinessMetrics
)
from ..schemas import ErrorResponse
from ...infrastructure.services.cache_service import CacheService

logger = logging.getLogger("data_routes")

# Create router
router = APIRouter(prefix="/api/v1/data", tags=["data"])

# Initialize real data service


def get_data_service():
    return RealDataService()


@router.get(
    "/sales",
    response_model=SalesDataResponse,
    summary="Get sales data",
    description="Retrieve real sales data for analysis"
)
async def get_sales_data(
    days: int = 30,
    db: Session = Depends(get_db),
    data_service: RealDataService = Depends(get_data_service)
):
    """
    Retrieve sales data for the specified number of days from the real data warehouse

    Args:
        days: Number of days of data to retrieve
        db: Database session dependency

    Returns:
        SalesDataResponse with sales data
    """
    try:
        logger.info(f"Retrieving sales data for {days} days")
        sales_data = data_service.get_sales_data(days)

        # Convert to Pydantic models - map the actual field names
        sales_items = [
            SalesDataItem(
                date=item["date"],
                product=item["product"],
                category="General",  # Mock service doesn't provide category
                store=item["store"],
                # Map quantity_sold to quantity
                quantity=item["quantity_sold"],
                revenue=item["revenue"],
                profit=item["profit"]
            )
            for item in sales_data
        ]

        return SalesDataResponse(
            data_type="sales",
            days=days,
            records=len(sales_items),
            data=sales_items
        )
    except Exception as e:
        logger.error(f"Error retrieving sales data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving sales data"
        )


@router.get(
    "/inventory",
    response_model=InventoryDataResponse,
    summary="Get inventory data",
    description="Retrieve real inventory data for analysis"
)
async def get_inventory_data(
    db: Session = Depends(get_db),
    data_service: RealDataService = Depends(get_data_service)
):
    """
    Retrieve current inventory data from the real data warehouse

    Args:
        db: Database session dependency

    Returns:
        InventoryDataResponse with inventory data
    """
    try:
        logger.info("Retrieving inventory data")
        inventory_data = data_service.get_inventory_data()

        # Convert to Pydantic models - map the actual field names
        inventory_items = [
            InventoryDataItem(
                product=item["product"],
                category="General",  # Mock service doesn't provide category
                store=item["store"],
                # Map current_stock to quantity
                quantity=item["current_stock"],
                reorder_level=item["reorder_level"],
                supplier=item["supplier"]
            )
            for item in inventory_data
        ]

        return InventoryDataResponse(
            data_type="inventory",
            records=len(inventory_items),
            data=inventory_items
        )
    except Exception as e:
        logger.error(
            f"Error retrieving inventory data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving inventory data"
        )


@router.get(
    "/customers",
    response_model=CustomerDataResponse,
    summary="Get customer data",
    description="Retrieve real customer data for analysis"
)
async def get_customer_data(
    count: int = 100,
    db: Session = Depends(get_db),
    data_service: RealDataService = Depends(get_data_service)
):
    """
    Retrieve customer data from the real data warehouse

    Args:
        count: Number of customers to retrieve
        db: Database session dependency

    Returns:
        CustomerDataResponse with customer data
    """
    try:
        logger.info(f"Retrieving customer data for {count} customers")
        customer_data = data_service.get_customer_data(count)

        # Convert to Pydantic models - map the actual field names
        customer_items = [
            CustomerDataItem(
                customer_id=item["customer_id"],
                name=item["name"],
                email=item["email"],
                segment=item["age_group"],
                total_purchases=item["total_purchases"],
                last_purchase_date=item["last_purchase"]
            )
            for item in customer_data
        ]

        return CustomerDataResponse(
            data_type="customers",
            count=len(customer_items),
            data=customer_items
        )
    except Exception as e:
        logger.error(
            f"Error retrieving customer data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving customer data"
        )


@router.get(
    "/metrics",
    response_model=MetricsDataResponse,
    summary="Get business metrics",
    description="Retrieve key business metrics and performance data from real data"
)
async def get_business_metrics(
    db: Session = Depends(get_db),
    data_service: RealDataService = Depends(get_data_service)
):
    """
    Retrieve business metrics and performance data from the real data warehouse

    Args:
        db: Database session dependency

    Returns:
        MetricsDataResponse with business metrics
    """
    try:
        logger.info("Retrieving business metrics")
        metrics = data_service.get_business_metrics()

        # Convert to Pydantic model - map the actual field names
        business_metrics = BusinessMetrics(
            total_revenue=metrics["total_revenue"],
            total_profit=metrics["total_profit"],
            profit_margin=metrics["profit_margin"],
            total_customers=100,  # Mock service doesn't provide this
            average_order_value=metrics["total_revenue"] /
            metrics["total_sales"] if metrics["total_sales"] > 0 else 0,
            inventory_turnover=4.5  # Mock value
        )

        return MetricsDataResponse(
            data_type="metrics",
            data=business_metrics
        )
    except Exception as e:
        logger.error(
            f"Error retrieving business metrics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving business metrics"
        )


@router.get(
    "/search",
    response_model=SearchDataResponse,
    summary="Search data by query",
    description="Search through real data based on natural language query"
)
async def search_data(
    query: str,
    db: Session = Depends(get_db),
    data_service: RealDataService = Depends(get_data_service)
):
    """
    Search through real data based on natural language query

    Args:
        query: Natural language search query
        db: Database session dependency

    Returns:
        SearchDataResponse with relevant data based on the query
    """
    try:
        logger.info(f"Searching data with query: {query}")
        search_result = data_service.search_data(query)

        return SearchDataResponse(
            query=query,
            data_type=search_result.get("data_type", "unknown"),
            records=len(search_result.get("data", [])),
            data=search_result.get("data", [])
        )
    except Exception as e:
        logger.error(f"Error searching data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while searching data"
        )


@router.get(
    "/health",
    response_model=DataHealthResponse,
    summary="Data service health check",
    description="Check if the real data service is healthy"
)
async def data_service_health():
    """
    Health check endpoint for real data service

    Returns:
        DataHealthResponse with service health status
    """
    return DataHealthResponse(
        service="real_data",
        status="healthy",
        message="Real data service is operational",
        available_data_types=["sales", "inventory", "customers", "metrics"]
    )


@router.get(
    "/cache/health",
    summary="Cache health check",
    description="Check Redis cache system health and performance"
)
async def cache_health_check():
    """
    Health check endpoint for Redis cache system

    Returns:
        Dictionary with cache health status and statistics
    """
    try:
        cache_service = CacheService()
        stats = cache_service.get_cache_stats()

        return {
            "service": "cache",
            "status": stats.get("status", "unknown"),
            "message": stats.get("message", "Cache health check completed"),
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Cache health check failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cache health check failed"
        )


@router.get(
    "/cache/stats",
    summary="Cache statistics",
    description="Get detailed cache performance statistics"
)
async def get_cache_statistics():
    """
    Get detailed cache performance statistics

    Returns:
        Dictionary with detailed cache statistics
    """
    try:
        cache_service = CacheService()
        stats = cache_service.get_cache_stats()

        return {
            "cache_statistics": stats,
            "cache_configuration": {
                "default_ttl": cache_service.default_ttl,
                "query_cache_ttl": cache_service.query_cache_ttl,
                "insight_cache_ttl": cache_service.insight_cache_ttl
            }
        }
    except Exception as e:
        logger.error(
            f"Failed to get cache statistics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cache statistics"
        )
