import logging
import os
from typing import Dict, Any, Optional, List
from openai import OpenAI
from datetime import datetime
import time
import instructor

from app.domain.entities.llm_models import QueryIntent, BusinessInsight, InsightResponse

logger = logging.getLogger("openai_service")


class OpenAIService:
    """
    Service for OpenAI API integration.
    Handles LLM calls with proper error handling, rate limiting, and cost tracking.
    Uses Instructor for deterministic structured data extraction.
    """

    def __init__(self):
        """Initialize OpenAI service with API key and Instructor client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
            self.client = None
            self.instructor_client = None
        else:
            self.client = OpenAI(api_key=api_key)
            # Initialize Instructor client for structured data extraction
            self.instructor_client = instructor.patch(self.client)

        # Cost tracking
        self.total_cost = 0.0
        self.total_tokens = 0

        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests

    def _wait_for_rate_limit(self):
        """Implement basic rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()

    def _track_cost(self, response: Any) -> float:
        """Track API call cost"""
        if hasattr(response, 'usage') and response.usage:
            tokens_used = response.usage.total_tokens
            # Approximate cost calculation (GPT-3.5-turbo pricing)
            cost_per_1k_tokens = 0.002  # $0.002 per 1K tokens
            cost = (tokens_used / 1000) * cost_per_1k_tokens

            self.total_tokens += tokens_used
            self.total_cost += cost

            logger.info(f"API call cost: ${cost:.4f}, tokens: {tokens_used}")
            return cost
        return 0.0

    def analyze_query_intent(self, query_text: str) -> Dict[str, Any]:
        """
        Analyze query intent using OpenAI with Instructor for deterministic parsing.

        Args:
            query_text: Natural language query

        Returns:
            Intent analysis with confidence and categories
        """
        if not self.instructor_client:
            logger.warning(
                "OpenAI client not available, using fallback intent analysis")
            return self._fallback_intent_analysis(query_text)

        try:
            self._wait_for_rate_limit()

            # Use Instructor for structured data extraction
            intent_analysis: QueryIntent = self.instructor_client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_model=QueryIntent,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a business intelligence analyst. Analyze the query intent and provide structured response."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze the following business query and determine its intent and relevant business categories: '{query_text}'"
                    }
                ],
                temperature=0.3,
                max_tokens=300
            )

            # Convert Pydantic model to dict for backward compatibility
            result = intent_analysis.model_dump()
            logger.info(
                f"Intent analysis completed: {result['intent']} (confidence: {result['confidence']})")
            return result

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
            return self._fallback_intent_analysis(query_text)

    def generate_insights(self, query_text: str, data_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate business insights using OpenAI with Instructor for deterministic parsing.

        Args:
            query_text: Original query
            data_context: Context data from mock data service

        Returns:
            List of generated insights
        """
        if not self.instructor_client:
            logger.warning(
                "OpenAI client not available, using fallback insights")
            return self._fallback_insights(query_text, data_context)

        try:
            self._wait_for_rate_limit()

            # Prepare data context for the prompt
            data_summary = self._summarize_data_context(data_context)

            # Use Instructor for structured data extraction
            insight_response: InsightResponse = self.instructor_client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_model=InsightResponse,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior business analyst. Generate actionable, data-driven insights based on the query and data context."
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Based on the following business query and data context, generate 2-3 actionable business insights.
                        
                        Query: "{query_text}"
                        
                        Data Context:
                        {data_summary}
                        
                        Focus on actionable insights that would help business decision-making.
                        """
                    }
                ],
                temperature=0.4,
                max_tokens=500
            )

            # Convert Pydantic models to dict for backward compatibility
            insights = [insight.model_dump()
                        for insight in insight_response.insights]
            logger.info(
                f"Generated {len(insights)} insights using OpenAI with Instructor")
            return insights

        except Exception as e:
            logger.error(
                f"OpenAI insights generation error: {str(e)}", exc_info=True)
            return self._fallback_insights(query_text, data_context)

    def _summarize_data_context(self, data_context: Dict[str, Any]) -> str:
        """Summarize data context for the prompt"""
        if not data_context:
            return "No specific data context available."

        data_type = data_context.get("data_type", "unknown")
        data = data_context.get("data", [])

        if data_type == "sales":
            if isinstance(data, list) and len(data) > 0:
                total_revenue = sum(item.get("revenue", 0) for item in data)
                total_profit = sum(item.get("profit", 0) for item in data)
                return f"Sales data: {len(data)} records, Total Revenue: ${total_revenue:.2f}, Total Profit: ${total_profit:.2f}"

        elif data_type == "metrics":
            metrics = data
            return f"Business metrics: Revenue: ${metrics.get('total_revenue', 0):.2f}, Profit: ${metrics.get('total_profit', 0):.2f}, Margin: {metrics.get('profit_margin', 0):.1f}%"

        return f"Data type: {data_type}, Records: {len(data) if isinstance(data, list) else 'N/A'}"

    def _fallback_intent_analysis(self, query_text: str) -> Dict[str, Any]:
        """Fallback intent analysis when OpenAI is not available"""
        text = query_text.lower()

        if any(word in text for word in ['trend', 'pattern', 'over time']):
            intent = 'trend_analysis'
        elif any(word in text for word in ['compare', 'vs', 'versus', 'difference']):
            intent = 'comparison'
        elif any(word in text for word in ['predict', 'forecast', 'future']):
            intent = 'prediction'
        elif any(word in text for word in ['why', 'cause', 'reason']):
            intent = 'root_cause'
        elif any(word in text for word in ['recommend', 'suggest', 'action']):
            intent = 'recommendation'
        else:
            intent = 'general_analysis'

        return {
            "intent": intent,
            "confidence": 0.6,
            "categories": ["sales", "performance"],
            "data_sources": ["sales_data"],
            "suggested_visualizations": ["line_chart"]
        }

    def _fallback_insights(self, query_text: str, data_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback insights when OpenAI is not available"""
        return [
            {
                "title": "General Business Analysis",
                "description": "Analysis based on available business data",
                "category": "general",
                "confidence_score": 0.6,
                "action_items": ["Review data regularly", "Monitor key metrics"],
                "data_evidence": "Based on query analysis"
            }
        ]

    def get_cost_summary(self) -> Dict[str, Any]:
        """Get cost tracking summary"""
        return {
            "total_cost": round(self.total_cost, 4),
            "total_tokens": self.total_tokens,
            "average_cost_per_request": round(self.total_cost / max(1, self.total_tokens / 1000), 4)
        }
