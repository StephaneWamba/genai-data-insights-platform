"""
Pydantic models for structured LLM responses using Instructor.
These models ensure deterministic parsing of LLM outputs.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class QueryIntent(BaseModel):
    """Structured model for query intent analysis"""
    intent: str = Field(
        description="The main intent of the query",
        examples=["trend_analysis", "comparison", "prediction",
                  "root_cause", "recommendation", "general_analysis"]
    )
    confidence: float = Field(
        description="Confidence score from 0.0 to 1.0",
        ge=0.0,
        le=1.0
    )
    categories: List[str] = Field(
        description="List of relevant business categories",
        examples=[["sales", "performance"], ["inventory", "customers"]]
    )
    data_sources: List[str] = Field(
        description="List of relevant data sources needed",
        examples=[["sales_data", "store_data"],
                  ["customer_data", "inventory_data"]]
    )
    suggested_visualizations: List[str] = Field(
        description="List of chart types that would be useful",
        examples=[["line_chart", "bar_chart"], ["pie_chart", "scatter_plot"]]
    )


class BusinessInsight(BaseModel):
    """Structured model for individual business insights"""
    title: str = Field(
        description="Short, descriptive title for the insight"
    )
    description: str = Field(
        description="Detailed insight description with actionable information"
    )
    category: str = Field(
        description="Category of the insight",
        examples=["trend", "anomaly", "recommendation",
                  "root_cause", "prediction"]
    )
    confidence_score: float = Field(
        description="Confidence score from 0.0 to 1.0",
        ge=0.0,
        le=1.0
    )
    action_items: List[str] = Field(
        description="List of specific action items or recommendations"
    )
    data_evidence: str = Field(
        description="Specific data points that support this insight"
    )


class InsightResponse(BaseModel):
    """Structured model for multiple insights response"""
    insights: List[BusinessInsight] = Field(
        description="List of generated business insights",
        min_items=1,
        max_items=5
    )
