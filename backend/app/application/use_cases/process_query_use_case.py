from typing import Optional, Dict, Any
from datetime import datetime
from ...domain.services import QueryProcessingService
from ...domain.entities.query import Query, QueryResult
from ...domain.entities.insight import Insight
from ...infrastructure.repositories import QueryRepository, InsightRepository


class ProcessQueryUseCase:
    """Use case for processing natural language queries"""

    def __init__(self, query_processing_service: QueryProcessingService, query_repository: QueryRepository, insight_repository: InsightRepository):
        """
        Initialize the use case with required services

        Args:
            query_processing_service: Domain service for query processing
            query_repository: Repository for query persistence
            insight_repository: Repository for insight persistence
        """
        self.query_processing_service = query_processing_service
        self.query_repository = query_repository
        self.insight_repository = insight_repository

    async def execute(self, query_text: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute the process query use case

        Args:
            query_text: Natural language query from user
            user_id: Optional user identifier (will be ignored for now)

        Returns:
            Dictionary containing query result and insights
        """
        # Step 1: Process and validate the query
        query = self.query_processing_service.process_query(
            query_text, None)  # Don't pass user_id for now

        # Step 2: Persist query to database
        query = self.query_repository.create(query)

        # Step 3: Analyze query intent
        intent = self.query_processing_service.analyze_query_intent(query)

        # Step 4: Get data context for insights
        data_context = self.query_processing_service.get_data_context(query)

        # Step 5: Generate insights based on intent
        insights = self.query_processing_service.generate_insights(
            query, intent, data_context)

        # Step 6: Persist insights to database
        insights = self.insight_repository.create_many(insights)

        # Step 7: Create query result
        query_result = self.query_processing_service.create_query_result(
            query, insights, intent)

        # Step 8: Mark query as processed and update in database
        query.processed = True
        query.response = "Query processed successfully"
        query = self.query_repository.update(query)

        # Step 9: Return structured response
        return {
            "success": True,
            "query": {
                "id": query.id,
                "text": query.text,
                "processed": query.processed,
                "created_at": query.created_at.isoformat()
            },
            "intent": intent,
            "insights": [
                {
                    "id": insight.id,
                    "title": insight.title,
                    "description": insight.description,
                    "category": insight.category,
                    "confidence_score": insight.confidence_score,
                    "data_sources": insight.data_sources
                }
                for insight in insights
            ],
            "recommendations": query_result.recommendations,
            "visualizations": query_result.visualizations,
            "processed_at": datetime.now().isoformat()
        }
