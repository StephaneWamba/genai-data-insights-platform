import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..entities.query import Query, QueryResult
from ..entities.insight import Insight
from ..value_objects import QueryText, ConfidenceScore
from ...infrastructure.services.openai_service import OpenAIService
from ...infrastructure.services.real_data_service import RealDataService
from ...infrastructure.services.dynamic_query_service import DynamicQueryService
from ...infrastructure.services.chart_generation_service import ChartGenerationService

logger = logging.getLogger(__name__)


class QueryProcessingService:
    """Domain service for processing natural language queries"""

    def __init__(self):
        """Initialize the query processing service"""
        self.openai_service = OpenAIService()
        self.data_service = RealDataService()
        self.dynamic_query_service = DynamicQueryService()
        self.chart_service = ChartGenerationService()

    def process_query(self, query_text: str, user_id: Optional[str] = None) -> Query:
        """
        Process a natural language query and create a Query entity

        Args:
            query_text: Natural language query from user
            user_id: Optional user identifier

        Returns:
            Query entity with processing status
        """
        # Validate query text using value object
        validated_text = QueryText(value=query_text)

        # Create query entity
        query = Query(
            text=validated_text.value,
            user_id=user_id,
            created_at=datetime.now(),
            processed=False
        )

        return query

    def analyze_query_intent(self, query: Query) -> Dict[str, Any]:
        """
        Analyze the intent of a query using OpenAI or fallback

        Args:
            query: Query entity to analyze

        Returns:
            Intent analysis with confidence and metadata
        """
        # Use OpenAI service for enhanced intent analysis
        intent_analysis = self.openai_service.analyze_query_intent(query.text)

        return intent_analysis

    def get_data_context(self, query: Query) -> Dict[str, Any]:
        """
        Get relevant data context for a query using dynamic database queries

        Args:
            query: Query entity

        Returns:
            Relevant data context from direct database queries
        """
        try:
            # Try dynamic query first for more accurate results
            dynamic_result = self.dynamic_query_service.query_database_directly(
                query.text)

            if dynamic_result.get("success") and dynamic_result.get("rows"):
                # Format dynamic query results for insight generation
                return {
                    "data_type": "dynamic_query",
                    "data": dynamic_result["rows"],
                    "columns": dynamic_result["columns"],
                    "row_count": dynamic_result["row_count"],
                    "sql_query": dynamic_result["sql_query"],
                    "data_sources": ["clickhouse_dynamic_query"]
                }
            else:
                # Fallback to traditional data service
                logger.warning(
                    f"Dynamic query failed, falling back to traditional data service: {dynamic_result.get('error', 'Unknown error')}")
                return self.data_service.search_data(query.text)

        except Exception as e:
            logger.error(
                f"Error in dynamic query, falling back to traditional data service: {e}")
            # Fallback to traditional data service
            return self.data_service.search_data(query.text)

    def get_relevant_data(self, query: Query, intent_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get relevant data based on query and intent analysis

        Args:
            query: Query entity
            intent_analysis: Intent analysis result

        Returns:
            Relevant data context
        """
        # Use mock data service to get relevant data
        data_context = self.data_service.search_data(query.text)

        return data_context

    def generate_insights(self, query: Query, intent_analysis: Dict[str, Any], data_context: Dict[str, Any]) -> List[Insight]:
        """
        Generate insights using OpenAI or fallback

        Args:
            query: Processed query entity
            intent_analysis: Intent analysis result
            data_context: Relevant data context

        Returns:
            List of generated insights
        """
        # Use OpenAI service for enhanced insight generation
        ai_insights = self.openai_service.generate_insights(
            query.text, data_context)

        insights = []
        temp_query_id = query.id if query.id is not None else 1

        for ai_insight in ai_insights:
            insight = Insight(
                query_id=temp_query_id,
                title=ai_insight.get("title", "Business Insight"),
                description=ai_insight.get(
                    "description", "Analysis based on business data"),
                category=ai_insight.get("category", "general"),
                confidence_score=ai_insight.get("confidence_score", 0.7),
                data_sources=data_context.get(
                    "data_sources", ["clickhouse_sales_data"])
            )
            insights.append(insight)

        # If no AI insights, use fallback
        if not insights:
            insights.append(Insight(
                query_id=temp_query_id,
                title="General Business Analysis",
                description="Analysis based on available business data",
                category="general",
                confidence_score=0.6,
                data_sources=["clickhouse_sales_data"]
            ))

        return insights

    def create_query_result(self, query: Query, insights: List[Insight], intent_analysis: Dict[str, Any], data_context: Dict[str, Any] = None) -> QueryResult:
        """
        Create a query result from processed query and insights with actual charts

        Args:
            query: Processed query entity
            insights: Generated insights
            intent_analysis: Intent analysis result
            data_context: Data context for chart generation

        Returns:
            QueryResult with insights, recommendations, and actual charts
        """
        # Extract recommendations from insights
        recommendations = []
        for insight in insights:
            if insight.category == 'trend':
                recommendations.append("Monitor trend continuation")
            elif insight.category == 'comparison':
                recommendations.append("Investigate performance differences")
            elif insight.category == 'recommendation':
                recommendations.append(
                    "Consider implementing suggested actions")
            else:
                recommendations.append(
                    "Review data regularly and monitor key metrics")

        # Generate actual charts if we have data context
        visualizations = []
        logger.info(
            f"Data context type: {data_context.get('data_type') if data_context else 'None'}")

        if data_context and data_context.get("data_type") == "dynamic_query":
            try:
                # Prepare query result for chart generation
                query_result = {
                    "success": True,
                    "rows": data_context.get("data", []),
                    "columns": data_context.get("columns", []),
                    "row_count": data_context.get("row_count", 0)
                }

                logger.info(
                    f"Preparing chart generation with {len(query_result['rows'])} rows and {len(query_result['columns'])} columns")

                # Get suggested chart types
                suggested_viz = intent_analysis.get(
                    "suggested_visualizations", ["bar_chart"])
                logger.info(f"Suggested visualizations: {suggested_viz}")

                # Generate charts for each suggested type
                for viz_type in suggested_viz[:2]:  # Limit to 2 charts
                    logger.info(f"Generating {viz_type} chart...")
                    chart_data = self.chart_service.generate_chart_data_from_query_result(
                        query_result, viz_type)
                    if "error" not in chart_data:
                        logger.info(f"Successfully generated {viz_type} chart")
                        visualizations.append(chart_data)
                    else:
                        logger.warning(
                            f"Failed to generate {viz_type} chart: {chart_data.get('error')}")

                # If no charts generated, try default bar chart
                if not visualizations:
                    logger.info(
                        "No charts generated, trying default bar chart...")
                    chart_data = self.chart_service.generate_chart_data_from_query_result(
                        query_result, "bar_chart")
                    if "error" not in chart_data:
                        logger.info("Successfully generated default bar chart")
                        visualizations.append(chart_data)
                    else:
                        logger.warning(
                            f"Failed to generate default bar chart: {chart_data.get('error')}")

            except Exception as e:
                logger.error(f"Error generating charts: {e}", exc_info=True)
                # Fallback to basic visualization config
                visualizations = [{
                    "type": "bar_chart",
                    "title": f"{intent_analysis.get('intent', 'analysis').title()} Visualization",
                    "data_source": "sales_data"
                }]
        else:
            # Fallback to basic visualization config
            suggested_viz = intent_analysis.get(
                "suggested_visualizations", ["bar_chart"])
            for viz_type in suggested_viz[:3]:
                visualizations.append({
                    "type": viz_type,
                    "title": f"{intent_analysis.get('intent', 'analysis').title()} Visualization",
                    "data_source": "sales_data"
                })

        return QueryResult(
            query_id=query.id if query.id is not None else 1,
            insights=[insight.description for insight in insights],
            recommendations=recommendations,
            visualizations=visualizations,
            created_at=datetime.now()
        )
