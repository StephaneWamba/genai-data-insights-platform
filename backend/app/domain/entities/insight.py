from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class Insight(BaseModel):
    """Insight entity representing AI-generated business insights"""

    id: Optional[int] = None
    query_id: int
    title: str
    description: str
    category: str  # e.g., 'trend', 'anomaly', 'recommendation'
    confidence_score: float
    data_sources: List[str]
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True


class InsightType:
    """Types of insights that can be generated"""

    TREND = "trend"
    ANOMALY = "anomaly"
    RECOMMENDATION = "recommendation"
    ROOT_CAUSE = "root_cause"
    PREDICTION = "prediction"
