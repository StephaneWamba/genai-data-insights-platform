from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class Query(BaseModel):
    """Query entity representing a natural language query"""

    id: Optional[int] = None
    text: str
    user_id: Optional[str] = None
    created_at: datetime = datetime.now()
    processed: bool = False
    response: Optional[str] = None

    class Config:
        from_attributes = True


class QueryResult(BaseModel):
    """Result of a processed query"""

    query_id: int
    insights: List[str]
    recommendations: List[str]
    visualizations: List[dict]
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True
