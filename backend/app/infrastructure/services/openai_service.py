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
                model="gpt-4o",
                response_model=QueryIntent,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior business intelligence analyst with expertise in data analysis and strategic insights. Analyze the query intent with high precision and provide structured response."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze the following business query and determine its intent and relevant business categories: '{query_text}'"
                    }
                ],
                temperature=0.2,
                max_tokens=500
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
                model="gpt-4o",
                response_model=InsightResponse,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior business analyst with expertise in data-driven decision making. Generate highly actionable, data-driven insights based on the query and concrete data context. Always reference specific numbers, trends, and data points in your insights. Provide strategic recommendations that are backed by the actual data provided."
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Based on the following business query and detailed data context, generate 2-3 highly actionable business insights.
                        
                        Query: "{query_text}"
                        
                        Data Context:
                        {data_summary}
                        
                        IMPORTANT: 
                        - Always reference specific numbers, percentages, and data points from the provided data
                        - Provide concrete, actionable recommendations based on the actual data
                        - Include specific product names, store locations, and financial figures when relevant
                        - Focus on insights that would help business decision-making with real impact
                        """
                    }
                ],
                temperature=0.1,
                max_tokens=800
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
        """Summarize data context for the prompt with detailed, concrete data"""
        if not data_context:
            return "No specific data context available."

        data_type = data_context.get("data_type", "unknown")
        data = data_context.get("data", [])

        if data_type == "sales":
            if isinstance(data, list) and len(data) > 0:
                total_revenue = sum(item.get("revenue", 0) for item in data)
                total_profit = sum(item.get("profit", 0) for item in data)

                # Get top products by revenue
                product_revenue = {}
                for item in data:
                    product = item.get("product", "Unknown")
                    revenue = item.get("revenue", 0)
                    product_revenue[product] = product_revenue.get(
                        product, 0) + revenue

                top_products = sorted(
                    product_revenue.items(), key=lambda x: x[1], reverse=True)[:5]

                # Get store performance
                store_revenue = {}
                for item in data:
                    store = item.get("store", "Unknown")
                    revenue = item.get("revenue", 0)
                    store_revenue[store] = store_revenue.get(
                        store, 0) + revenue

                top_stores = sorted(store_revenue.items(),
                                    key=lambda x: x[1], reverse=True)[:3]

                profit_margin = (total_profit/total_revenue *
                                 100) if total_revenue > 0 else 0
                summary = f"""
SALES DATA ANALYSIS:
- Total Records: {len(data)} sales transactions
- Total Revenue: ${total_revenue:,.2f}
- Total Profit: ${total_profit:,.2f}
- Profit Margin: {profit_margin:.1f}%

TOP 5 PRODUCTS BY REVENUE:
{chr(10).join([f"- {product}: ${revenue:,.2f}" for product, revenue in top_products])}

TOP 3 STORES BY REVENUE:
{chr(10).join([f"- {store}: ${revenue:,.2f}" for store, revenue in top_stores])}

SAMPLE TRANSACTIONS (first 5):
{chr(10).join([f"- {item.get('date', 'N/A')}: {item.get('product', 'N/A')} at {item.get('store', 'N/A')} - Qty: {item.get('quantity_sold', 0)}, Revenue: ${item.get('revenue', 0):,.2f}, Profit: ${item.get('profit', 0):,.2f}" for item in data[:5]])}
"""
                return summary

        elif data_type == "metrics":
            metrics = data
            return f"""
BUSINESS METRICS:
- Total Revenue: ${metrics.get('total_revenue', 0):,.2f}
- Total Profit: ${metrics.get('total_profit', 0):,.2f}
- Profit Margin: {metrics.get('profit_margin', 0):.1f}%
- Total Customers: {metrics.get('total_customers', 0)}
- Average Order Value: ${metrics.get('average_order_value', 0):,.2f}
- Inventory Turnover: {metrics.get('inventory_turnover', 0)}
"""

        elif data_type == "inventory":
            if isinstance(data, list) and len(data) > 0:
                total_stock = sum(item.get("current_stock", 0)
                                  for item in data)
                low_stock_items = [item for item in data if item.get(
                    "current_stock", 0) <= item.get("reorder_level", 0)]

                summary = f"""
INVENTORY DATA:
- Total Items: {len(data)} products
- Total Stock: {total_stock} units
- Low Stock Items: {len(low_stock_items)} products below reorder level

LOW STOCK ALERTS:
{chr(10).join([f"- {item.get('product', 'N/A')} at {item.get('store', 'N/A')}: {item.get('current_stock', 0)} units (reorder level: {item.get('reorder_level', 0)})" for item in low_stock_items[:5]])}
"""
                return summary

        elif data_type == "customers":
            if isinstance(data, list) and len(data) > 0:
                total_purchases = sum(item.get("total_purchases", 0)
                                      for item in data)
                avg_purchases = total_purchases / len(data) if data else 0

                summary = f"""
CUSTOMER DATA:
- Total Customers: {len(data)} customers
- Total Purchases: {total_purchases:,.0f}
- Average Purchases per Customer: {avg_purchases:.1f}

SAMPLE CUSTOMERS:
{chr(10).join([f"- {item.get('name', 'N/A')} ({item.get('email', 'N/A')}): {item.get('total_purchases', 0):,.0f} purchases, Last: {item.get('last_purchase', 'N/A')}" for item in data[:5]])}
"""
                return summary

        elif data_type == "dynamic_query":
            if isinstance(data, list) and len(data) > 0:
                columns = data_context.get("columns", [])
                sql_query = data_context.get("sql_query", "N/A")

                summary = f"""
DYNAMIC DATABASE QUERY RESULTS:
- SQL Query: {sql_query}
- Columns: {', '.join(columns)}
- Total Rows: {len(data)} records

QUERY RESULTS (first 10 rows):
"""
                for i, row in enumerate(data[:10]):
                    row_summary = []
                    for col in columns:
                        value = row.get(col, "N/A")
                        if isinstance(value, (int, float)):
                            row_summary.append(f"{col}: {value:,.2f}")
                        else:
                            row_summary.append(f"{col}: {value}")
                    summary += f"\nRow {i+1}: {', '.join(row_summary)}"

                return summary

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
            "suggested_visualizations": ["bar_chart", "line_chart", "pie_chart", "doughnut_chart", "scatter_plot", "bubble_chart", "radar_chart", "horizontal_bar_chart", "stacked_bar_chart", "multi_line_chart", "area_chart"]
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
