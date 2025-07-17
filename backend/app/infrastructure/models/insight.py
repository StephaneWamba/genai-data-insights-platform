from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey, ARRAY, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Insight(Base):
    """Insight database model"""

    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=False)
    data_sources = Column(ARRAY(String), nullable=True)

    # Relationships
    query = relationship("Query", back_populates="insights")
