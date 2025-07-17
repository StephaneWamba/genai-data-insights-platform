from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Query(Base):
    """Query database model"""

    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    text = Column(Text, nullable=False)
    # Changed to String and nullable
    user_id = Column(String(100), nullable=True)
    processed = Column(Boolean, default=False)
    response = Column(Text, nullable=True)

    # Relationships
    insights = relationship("Insight", back_populates="query")
    results = relationship("QueryResult", back_populates="query")
    # user = relationship("User", back_populates="queries")
