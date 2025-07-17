from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class SalesDataItem(BaseModel):
    """Schema for individual sales data item"""

    date: str = Field(..., description="Sale date")
    product: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    store: str = Field(..., description="Store location")
    quantity: int = Field(..., ge=0, description="Quantity sold")
    revenue: float = Field(..., ge=0, description="Revenue amount")
    profit: float = Field(..., description="Profit amount")

    class Config:
        schema_extra = {
            "example": {
                "date": "2024-01-15",
                "product": "Running Shoes",
                "category": "Footwear",
                "store": "Paris Store",
                "quantity": 5,
                "revenue": 750.00,
                "profit": 150.00
            }
        }


class InventoryDataItem(BaseModel):
    """Schema for individual inventory data item"""

    product: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    store: str = Field(..., description="Store location")
    quantity: int = Field(..., ge=0, description="Current stock quantity")
    reorder_level: int = Field(..., ge=0, description="Reorder threshold")
    supplier: str = Field(..., description="Supplier name")

    class Config:
        schema_extra = {
            "example": {
                "product": "Running Shoes",
                "category": "Footwear",
                "store": "Paris Store",
                "quantity": 25,
                "reorder_level": 10,
                "supplier": "SportsCorp"
            }
        }


class CustomerDataItem(BaseModel):
    """Schema for individual customer data item"""

    customer_id: str = Field(..., description="Customer ID")
    name: str = Field(..., description="Customer name")
    email: str = Field(..., description="Customer email")
    segment: str = Field(..., description="Customer segment")
    total_purchases: float = Field(..., ge=0,
                                   description="Total purchase amount")
    last_purchase_date: str = Field(..., description="Last purchase date")

    class Config:
        schema_extra = {
            "example": {
                "customer_id": "CUST001",
                "name": "John Doe",
                "email": "john.doe@email.com",
                "segment": "Premium",
                "total_purchases": 2500.00,
                "last_purchase_date": "2024-01-10"
            }
        }


class BusinessMetrics(BaseModel):
    """Schema for business metrics"""

    total_revenue: float = Field(..., ge=0, description="Total revenue")
    total_profit: float = Field(..., description="Total profit")
    profit_margin: float = Field(..., ge=0, le=100,
                                 description="Profit margin percentage")
    total_customers: int = Field(..., ge=0,
                                 description="Total number of customers")
    average_order_value: float = Field(...,
                                       ge=0, description="Average order value")
    inventory_turnover: float = Field(..., ge=0,
                                      description="Inventory turnover rate")

    class Config:
        schema_extra = {
            "example": {
                "total_revenue": 150000.00,
                "total_profit": 30000.00,
                "profit_margin": 20.0,
                "total_customers": 1250,
                "average_order_value": 120.00,
                "inventory_turnover": 4.5
            }
        }


class SalesDataResponse(BaseModel):
    """Schema for sales data response"""

    data_type: str = Field("sales", description="Data type")
    days: int = Field(..., description="Number of days of data")
    records: int = Field(..., description="Number of records")
    data: List[SalesDataItem] = Field(..., description="Sales data records")

    class Config:
        schema_extra = {
            "example": {
                "data_type": "sales",
                "days": 30,
                "records": 150,
                "data": [
                    {
                        "date": "2024-01-15",
                        "product": "Running Shoes",
                        "category": "Footwear",
                        "store": "Paris Store",
                        "quantity": 5,
                        "revenue": 750.00,
                        "profit": 150.00
                    }
                ]
            }
        }


class InventoryDataResponse(BaseModel):
    """Schema for inventory data response"""

    data_type: str = Field("inventory", description="Data type")
    records: int = Field(..., description="Number of records")
    data: List[InventoryDataItem] = Field(...,
                                          description="Inventory data records")

    class Config:
        schema_extra = {
            "example": {
                "data_type": "inventory",
                "records": 50,
                "data": [
                    {
                        "product": "Running Shoes",
                        "category": "Footwear",
                        "store": "Paris Store",
                        "quantity": 25,
                        "reorder_level": 10,
                        "supplier": "SportsCorp"
                    }
                ]
            }
        }


class CustomerDataResponse(BaseModel):
    """Schema for customer data response"""

    data_type: str = Field("customers", description="Data type")
    count: int = Field(..., description="Number of customers")
    data: List[CustomerDataItem] = Field(...,
                                         description="Customer data records")

    class Config:
        schema_extra = {
            "example": {
                "data_type": "customers",
                "count": 100,
                "data": [
                    {
                        "customer_id": "CUST001",
                        "name": "John Doe",
                        "email": "john.doe@email.com",
                        "segment": "Premium",
                        "total_purchases": 2500.00,
                        "last_purchase_date": "2024-01-10"
                    }
                ]
            }
        }


class MetricsDataResponse(BaseModel):
    """Schema for business metrics response"""

    data_type: str = Field("metrics", description="Data type")
    data: BusinessMetrics = Field(..., description="Business metrics")

    class Config:
        schema_extra = {
            "example": {
                "data_type": "metrics",
                "data": {
                    "total_revenue": 150000.00,
                    "total_profit": 30000.00,
                    "profit_margin": 20.0,
                    "total_customers": 1250,
                    "average_order_value": 120.00,
                    "inventory_turnover": 4.5
                }
            }
        }


class SearchDataResponse(BaseModel):
    """Schema for data search response"""

    query: str = Field(..., description="Search query")
    data_type: str = Field(..., description="Type of data found")
    records: int = Field(..., description="Number of matching records")
    data: List[Dict[str, Any]
               ] = Field(..., description="Matching data records")

    class Config:
        schema_extra = {
            "example": {
                "query": "sales trends",
                "data_type": "sales",
                "records": 25,
                "data": [
                    {
                        "date": "2024-01-15",
                        "product": "Running Shoes",
                        "revenue": 750.00
                    }
                ]
            }
        }


class HealthResponse(BaseModel):
    """Schema for health check responses"""

    service: str = Field(..., description="Service name")
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    available_data_types: List[str] = Field(...,
                                            description="Available data types")

    class Config:
        schema_extra = {
            "example": {
                "service": "mock_data",
                "status": "healthy",
                "message": "Mock data service is operational",
                "available_data_types": ["sales", "inventory", "customers", "metrics"]
            }
        }
