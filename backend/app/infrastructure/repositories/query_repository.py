from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.query import Query as QueryModel
from ...domain.entities.query import Query
from datetime import datetime


class QueryRepository:
    """
    Repository for managing Query persistence.
    Provides CRUD operations for Query objects.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with SQLAlchemy session.
        Args:
            db: SQLAlchemy session
        """
        self.db = db

    def create(self, query: Query) -> Query:
        """
        Persist a new Query to the database.
        Args:
            query: Query domain entity
        Returns:
            Query domain entity with ID
        """
        db_query = QueryModel(
            text=query.text,
            user_id=query.user_id,
            created_at=query.created_at or datetime.utcnow(),
            processed=query.processed,
            response=query.response
        )
        self.db.add(db_query)
        self.db.commit()
        self.db.refresh(db_query)
        query.id = db_query.id
        return query

    def get_by_id(self, query_id: int) -> Optional[Query]:
        """
        Retrieve a Query by its ID.
        Args:
            query_id: Query ID
        Returns:
            Query domain entity or None
        """
        db_query = self.db.query(QueryModel).filter(
            QueryModel.id == query_id).first()
        if db_query:
            return Query(
                id=db_query.id,
                text=db_query.text,
                user_id=db_query.user_id,
                created_at=db_query.created_at,
                processed=db_query.processed,
                response=db_query.response
            )
        return None

    def list_by_user(self, user_id: str) -> List[Query]:
        """
        List all queries for a given user.
        Args:
            user_id: User identifier
        Returns:
            List of Query domain entities
        """
        db_queries = self.db.query(QueryModel).filter(
            QueryModel.user_id == user_id).all()
        return [
            Query(
                id=q.id,
                text=q.text,
                user_id=q.user_id,
                created_at=q.created_at,
                processed=q.processed,
                response=q.response
            ) for q in db_queries
        ]

    def update(self, query: Query) -> Query:
        """
        Update an existing Query in the database.
        Args:
            query: Query domain entity
        Returns:
            Updated Query domain entity
        """
        db_query = self.db.query(QueryModel).filter(
            QueryModel.id == query.id).first()
        if not db_query:
            raise ValueError("Query not found")
        db_query.text = query.text
        db_query.processed = query.processed
        db_query.response = query.response
        self.db.commit()
        self.db.refresh(db_query)
        return query
