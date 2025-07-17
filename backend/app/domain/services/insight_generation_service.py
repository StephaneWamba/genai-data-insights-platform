from typing import List, Dict, Any
from datetime import datetime
from ..entities.insight import Insight, InsightType
from ...infrastructure.services.openai_service import OpenAIService
from ...infrastructure.services.cache_service import CacheService


class InsightGenerationService:
    """
    Domain service for generating business insights from queries and data.
    Handles AI-powered insight generation with caching and fallback mechanisms.
    """

    def __init__(self):
        """Initialize the insight generation service"""
        self.openai_service = OpenAIService()
        self.cache_service = CacheService()

    def generate_insights(self, query_text: str, data_context: Dict[str, Any], query_id: int) -> List[Insight]:
        """
        Generate business insights using AI and caching

        Args:
            query_text: Natural language query
            data_context: Relevant data context
            query_id: Query identifier for caching

        Returns:
            List of generated insights
        """
        # Check cache first
        cached_insights = self.cache_service.get_cached_insights(query_id)
        if cached_insights:
            return [Insight(**insight) for insight in cached_insights]

        # Generate insights using AI
        ai_insights = self._generate_ai_insights(query_text, data_context)

        # Convert to domain entities
        insights = self._convert_to_insights(
            ai_insights, query_id, data_context)

        # Cache the insights
        insight_data = [insight.model_dump() for insight in insights]
        self.cache_service.cache_insights(query_id, insight_data)

        return insights

    def _generate_ai_insights(self, query_text: str, data_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights using OpenAI service

        Args:
            query_text: Natural language query
            data_context: Relevant data context

        Returns:
            List of AI-generated insights
        """
        try:
            return self.openai_service.generate_insights(query_text, data_context)
        except Exception as e:
            # Fallback to basic insights if AI fails
            return self._generate_fallback_insights(query_text, data_context)

    def _convert_to_insights(self, ai_insights: List[Dict[str, Any]], query_id: int, data_context: Dict[str, Any]) -> List[Insight]:
        """
        Convert AI insights to domain entities

        Args:
            ai_insights: AI-generated insights
            query_id: Query identifier
            data_context: Data context

        Returns:
            List of Insight entities
        """
        insights = []

        for ai_insight in ai_insights:
            insight = Insight(
                query_id=query_id,
                title=ai_insight.get("title", "Business Insight"),
                description=ai_insight.get(
                    "description", "Analysis based on business data"),
                category=ai_insight.get(
                    "category", InsightType.RECOMMENDATION),
                confidence_score=ai_insight.get("confidence_score", 0.7),
                data_sources=data_context.get("data_sources", ["mock_data"]),
                created_at=datetime.now()
            )
            insights.append(insight)

        # Ensure at least one insight is returned
        if not insights:
            insights.append(self._create_default_insight(
                query_id, data_context))

        return insights

    def _generate_fallback_insights(self, query_text: str, data_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate fallback insights when AI is unavailable

        Args:
            query_text: Natural language query
            data_context: Relevant data context

        Returns:
            List of fallback insights
        """
        # Basic pattern matching for fallback insights
        text_lower = query_text.lower()

        insights = []

        if any(word in text_lower for word in ['trend', 'pattern', 'over time']):
            insights.append({
                "title": "Trend Analysis",
                "description": "Consider analyzing historical patterns to identify trends in your data",
                "category": InsightType.TREND,
                "confidence_score": 0.6
            })

        if any(word in text_lower for word in ['compare', 'vs', 'versus', 'difference']):
            insights.append({
                "title": "Comparative Analysis",
                "description": "Compare different segments or time periods to identify performance differences",
                "category": InsightType.ANOMALY,
                "confidence_score": 0.6
            })

        if any(word in text_lower for word in ['why', 'cause', 'reason']):
            insights.append({
                "title": "Root Cause Analysis",
                "description": "Investigate underlying factors that may be causing observed patterns",
                "category": InsightType.ROOT_CAUSE,
                "confidence_score": 0.6
            })

        if any(word in text_lower for word in ['recommend', 'suggest', 'action']):
            insights.append({
                "title": "Actionable Recommendations",
                "description": "Consider implementing data-driven recommendations to improve performance",
                "category": InsightType.RECOMMENDATION,
                "confidence_score": 0.6
            })

        # Default insight if no patterns match
        if not insights:
            insights.append({
                "title": "General Business Analysis",
                "description": "Review your business data regularly and monitor key performance indicators",
                "category": InsightType.RECOMMENDATION,
                "confidence_score": 0.5
            })

        return insights

    def _create_default_insight(self, query_id: int, data_context: Dict[str, Any]) -> Insight:
        """
        Create a default insight when no AI insights are available

        Args:
            query_id: Query identifier
            data_context: Data context

        Returns:
            Default insight entity
        """
        return Insight(
            query_id=query_id,
            title="General Business Analysis",
            description="Analysis based on available business data. Consider reviewing key metrics and trends.",
            category=InsightType.RECOMMENDATION,
            confidence_score=0.5,
            data_sources=data_context.get("data_sources", ["mock_data"]),
            created_at=datetime.now()
        )

    def get_insight_recommendations(self, insights: List[Insight]) -> List[str]:
        """
        Generate actionable recommendations from insights

        Args:
            insights: List of insights

        Returns:
            List of actionable recommendations
        """
        recommendations = []

        for insight in insights:
            if insight.category == InsightType.TREND:
                recommendations.append(
                    "Monitor trend continuation and set up alerts for significant changes")
            elif insight.category == InsightType.ANOMALY:
                recommendations.append(
                    "Investigate performance differences and identify contributing factors")
            elif insight.category == InsightType.ROOT_CAUSE:
                recommendations.append(
                    "Address underlying issues and implement preventive measures")
            elif insight.category == InsightType.RECOMMENDATION:
                recommendations.append(
                    "Consider implementing suggested actions and track their impact")
            elif insight.category == InsightType.PREDICTION:
                recommendations.append(
                    "Prepare for predicted scenarios and develop contingency plans")
            else:
                recommendations.append(
                    "Review data regularly and monitor key metrics for opportunities")

        return recommendations

    def categorize_insights(self, insights: List[Insight]) -> Dict[str, List[Insight]]:
        """
        Categorize insights by type for better organization

        Args:
            insights: List of insights

        Returns:
            Dictionary of insights grouped by category
        """
        categorized = {
            InsightType.TREND: [],
            InsightType.ANOMALY: [],
            InsightType.RECOMMENDATION: [],
            InsightType.ROOT_CAUSE: [],
            InsightType.PREDICTION: []
        }

        for insight in insights:
            if insight.category in categorized:
                categorized[insight.category].append(insight)
            else:
                categorized[InsightType.RECOMMENDATION].append(insight)

        return categorized
