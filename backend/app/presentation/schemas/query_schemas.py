from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class QueryRequest(BaseModel):
    """Schema for query request from client"""

    query_text: str = Field(..., min_length=1, max_length=1000,
                            description="Natural language query")
    user_id: Optional[str] = Field(
        None, description="Optional user identifier")

    class Config:
        schema_extra = {
            "example": {
                "query_text": "What are the sales trends for shoes in Paris stores this quarter?",
                "user_id": "user123"
            }
        }


class QueryInfo(BaseModel):
    """Schema for query information in responses"""

    id: int = Field(..., description="Query ID")
    text: str = Field(..., description="Query text")
    user_id: Optional[str] = Field(None, description="User ID")
    processed: bool = Field(..., description="Processing status")
    response: Optional[str] = Field(None, description="Query response")
    created_at: str = Field(..., description="Creation timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "text": "What are the sales trends for shoes in Paris stores this quarter?",
                "user_id": "user123",
                "processed": True,
                "response": "Query processed successfully",
                "created_at": "2024-01-15T10:30:00"
            }
        }


class InsightResponse(BaseModel):
    """Schema for insight response"""

    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Insight description")
    category: str = Field(..., description="Insight category")
    confidence_score: float = Field(..., ge=0.0,
                                    le=1.0, description="AI confidence score")
    data_sources: List[str] = Field(..., description="Data sources used")

    class Config:
        schema_extra = {
            "example": {
                "title": "Sales Trend Analysis",
                "description": "Analyzing sales patterns over time",
                "category": "trend",
                "confidence_score": 0.85,
                "data_sources": ["sales_data", "inventory_data"]
            }
        }


class VisualizationResponse(BaseModel):
    """Schema for visualization response"""

    type: str = Field(..., description="Chart type")
    title: str = Field(..., description="Visualization title")
    data_source: str = Field(..., description="Data source for visualization")

    class Config:
        schema_extra = {
            "example": {
                "type": "line_chart",
                "title": "Trend Analysis",
                "data_source": "sales_data"
            }
        }


class QueryResponse(BaseModel):
    """Schema for successful query response"""

    success: bool = Field(True, description="Operation success status")
    query: QueryInfo = Field(..., description="Query information")
    intent: Dict[str, Any] = Field(..., description="Analyzed query intent")
    insights: List[InsightResponse] = Field(...,
                                            description="Generated insights")
    recommendations: List[str] = Field(...,
                                       description="Action recommendations")
    visualizations: List[VisualizationResponse] = Field(
        ..., description="Suggested visualizations")
    processed_at: str = Field(..., description="Processing timestamp")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "query": {
                    "id": 1,
                    "text": "What are the sales trends for shoes in Paris stores this quarter?",
                    "user_id": "user123",
                    "processed": True,
                    "response": "Query processed successfully",
                    "created_at": "2024-01-15T10:30:00"
                },
                "intent": {
                    "intent": "trend_analysis",
                    "confidence": 0.85,
                    "categories": ["sales", "performance"]
                },
                "insights": [
                    {
                        "title": "Sales Trend Analysis",
                        "description": "Analyzing sales patterns over time",
                        "category": "trend",
                        "confidence_score": 0.85,
                        "data_sources": ["sales_data", "inventory_data"]
                    }
                ],
                "recommendations": ["Monitor trend continuation"],
                "visualizations": [
                    {
                        "type": "line_chart",
                        "title": "Trend Analysis",
                        "data_source": "sales_data"
                    }
                ],
                "processed_at": "2024-01-15T10:30:05"
            }
        }


class QueryDetailResponse(BaseModel):
    """Schema for query detail response (GET by ID)"""

    query: QueryInfo = Field(..., description="Query information")

    class Config:
        schema_extra = {
            "example": {
                "query": {
                    "id": 1,
                    "text": "What are the sales trends for shoes in Paris stores this quarter?",
                    "user_id": "user123",
                    "processed": True,
                    "response": "Query processed successfully",
                    "created_at": "2024-01-15T10:30:00"
                }
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
                "service": "query_processing",
                "status": "healthy",
                "message": "Query processing service is operational"
            }
        }


class ErrorResponse(BaseModel):
    """Schema for error responses"""

    success: bool = Field(False, description="Operation success status")
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    processed_at: str = Field(..., description="Processing timestamp")

    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": "Validation error",
                "message": "Query should be a question or analysis request",
                "processed_at": "2024-01-15T10:30:00"
            }
        }
