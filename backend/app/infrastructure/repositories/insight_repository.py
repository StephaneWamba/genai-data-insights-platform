from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.insight import Insight as InsightModel
from ...domain.entities.insight import Insight
from datetime import datetime


class InsightRepository:
    """
    Repository for managing Insight persistence.
    Provides CRUD operations for Insight objects.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with SQLAlchemy session.
        Args:
            db: SQLAlchemy session
        """
        self.db = db

    def create(self, insight: Insight) -> Insight:
        """
        Persist a new Insight to the database.
        Args:
            insight: Insight domain entity
        Returns:
            Insight domain entity with ID
        """
        db_insight = InsightModel(
            query_id=insight.query_id,
            title=insight.title,
            description=insight.description,
            category=insight.category,
            confidence_score=insight.confidence_score,
            data_sources=insight.data_sources,
            created_at=insight.created_at or datetime.utcnow()
        )
        self.db.add(db_insight)
        self.db.commit()
        self.db.refresh(db_insight)
        insight.id = db_insight.id
        return insight

    def create_many(self, insights: List[Insight]) -> List[Insight]:
        """
        Persist multiple insights to the database.
        Args:
            insights: List of Insight domain entities
        Returns:
            List of Insight domain entities with IDs
        """
        db_insights = []
        for insight in insights:
            db_insight = InsightModel(
                query_id=insight.query_id,
                title=insight.title,
                description=insight.description,
                category=insight.category,
                confidence_score=insight.confidence_score,
                data_sources=insight.data_sources,
                created_at=insight.created_at or datetime.utcnow()
            )
            db_insights.append(db_insight)

        self.db.add_all(db_insights)
        self.db.commit()

        # Refresh and update domain entities with IDs
        for i, db_insight in enumerate(db_insights):
            self.db.refresh(db_insight)
            insights[i].id = db_insight.id

        return insights

    def get_by_id(self, insight_id: int) -> Optional[Insight]:
        """
        Retrieve an Insight by its ID.
        Args:
            insight_id: Insight ID
        Returns:
            Insight domain entity or None
        """
        db_insight = self.db.query(InsightModel).filter(
            InsightModel.id == insight_id).first()
        if db_insight:
            return Insight(
                id=db_insight.id,
                query_id=db_insight.query_id,
                title=db_insight.title,
                description=db_insight.description,
                category=db_insight.category,
                confidence_score=db_insight.confidence_score,
                data_sources=db_insight.data_sources,
                created_at=db_insight.created_at
            )
        return None

    def get_by_query_id(self, query_id: int) -> List[Insight]:
        """
        Retrieve all insights for a specific query.
        Args:
            query_id: Query ID
        Returns:
            List of Insight domain entities
        """
        db_insights = self.db.query(InsightModel).filter(
            InsightModel.query_id == query_id).all()
        return [
            Insight(
                id=insight.id,
                query_id=insight.query_id,
                title=insight.title,
                description=insight.description,
                category=insight.category,
                confidence_score=insight.confidence_score,
                data_sources=insight.data_sources,
                created_at=insight.created_at
            ) for insight in db_insights
        ]

    def get_by_category(self, category: str) -> List[Insight]:
        """
        Retrieve insights by category.
        Args:
            category: Insight category
        Returns:
            List of Insight domain entities
        """
        db_insights = self.db.query(InsightModel).filter(
            InsightModel.category == category).all()
        return [
            Insight(
                id=insight.id,
                query_id=insight.query_id,
                title=insight.title,
                description=insight.description,
                category=insight.category,
                confidence_score=insight.confidence_score,
                data_sources=insight.data_sources,
                created_at=insight.created_at
            ) for insight in db_insights
        ]

    def update(self, insight: Insight) -> Insight:
        """
        Update an existing Insight in the database.
        Args:
            insight: Insight domain entity
        Returns:
            Updated Insight domain entity
        """
        db_insight = self.db.query(InsightModel).filter(
            InsightModel.id == insight.id).first()
        if not db_insight:
            raise ValueError("Insight not found")

        db_insight.title = insight.title
        db_insight.description = insight.description
        db_insight.category = insight.category
        db_insight.confidence_score = insight.confidence_score
        db_insight.data_sources = insight.data_sources

        self.db.commit()
        self.db.refresh(db_insight)
        return insight
