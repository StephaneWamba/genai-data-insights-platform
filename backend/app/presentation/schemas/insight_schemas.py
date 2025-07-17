from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class InsightInfo(BaseModel):
    """Schema for insight information in responses"""

    id: int = Field(..., description="Insight ID")
    query_id: int = Field(..., description="Associated query ID")
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Insight description")
    category: str = Field(..., description="Insight category")
    confidence_score: float = Field(..., ge=0.0,
                                    le=1.0, description="AI confidence score")
    data_sources: List[str] = Field(..., description="Data sources used")
    created_at: str = Field(..., description="Creation timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "query_id": 1,
                "title": "Sales Trend Analysis",
                "description": "Analyzing sales patterns over time",
                "category": "trend",
                "confidence_score": 0.85,
                "data_sources": ["sales_data", "inventory_data"],
                "created_at": "2024-01-15T10:30:00"
            }
        }


class InsightDetailResponse(BaseModel):
    """Schema for single insight response (GET by ID)"""

    insight: InsightInfo = Field(..., description="Insight information")

    class Config:
        schema_extra = {
            "example": {
                "insight": {
                    "id": 1,
                    "query_id": 1,
                    "title": "Sales Trend Analysis",
                    "description": "Analyzing sales patterns over time",
                    "category": "trend",
                    "confidence_score": 0.85,
                    "data_sources": ["sales_data", "inventory_data"],
                    "created_at": "2024-01-15T10:30:00"
                }
            }
        }


class InsightListResponse(BaseModel):
    """Schema for list of insights response"""

    insights: List[InsightInfo] = Field(..., description="List of insights")
    count: int = Field(..., description="Total number of insights")

    class Config:
        schema_extra = {
            "example": {
                "insights": [
                    {
                        "id": 1,
                        "query_id": 1,
                        "title": "Sales Trend Analysis",
                        "description": "Analyzing sales patterns over time",
                        "category": "trend",
                        "confidence_score": 0.85,
                        "data_sources": ["sales_data", "inventory_data"],
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
                "service": "insight_processing",
                "status": "healthy",
                "message": "Insight service is operational"
            }
        }
