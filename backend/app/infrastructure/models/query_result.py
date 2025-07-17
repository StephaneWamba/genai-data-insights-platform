from sqlalchemy import Column, Integer, ForeignKey, Text, ARRAY, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class QueryResult(Base):
    """QueryResult database model"""

    __tablename__ = "query_results"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    insights = Column(ARRAY(Text), nullable=True)
    recommendations = Column(ARRAY(Text), nullable=True)
    visualizations = Column(JSON, nullable=True)

    # Relationships
    query = relationship("Query", back_populates="results")
