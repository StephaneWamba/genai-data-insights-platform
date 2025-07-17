from typing import List, Dict, Any
from datetime import datetime


class VisualizationService:
    """
    Domain service for generating visualizations based on query intent and data.
    Handles chart type selection and visualization configuration.
    """

    def __init__(self):
        """Initialize the visualization service"""
        self.chart_types = {
            "trend_analysis": ["line_chart", "area_chart", "bar_chart"],
            "comparison": ["bar_chart", "column_chart", "pie_chart"],
            "distribution": ["histogram", "box_plot", "scatter_plot"],
            "correlation": ["scatter_plot", "heatmap", "bubble_chart"],
            "prediction": ["line_chart", "area_chart", "forecast_chart"],
            "root_cause": ["bar_chart", "funnel_chart", "tree_map"]
        }

    def generate_visualizations(self, intent_analysis: Dict[str, Any], data_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate visualizations based on query intent and data context

        Args:
            intent_analysis: Intent analysis result
            data_context: Relevant data context

        Returns:
            List of visualization configurations
        """
        intent = intent_analysis.get("intent", "general_analysis")
        suggested_viz = intent_analysis.get("suggested_visualizations", [])

        # Get appropriate chart types for the intent
        chart_types = self._get_chart_types_for_intent(intent)

        # Combine suggested visualizations with intent-based ones
        all_chart_types = list(set(suggested_viz + chart_types))

        visualizations = []
        # Limit to 3 visualizations
        for i, chart_type in enumerate(all_chart_types[:3]):
            viz_config = self._create_visualization_config(
                chart_type, intent, data_context, i + 1
            )
            visualizations.append(viz_config)

        return visualizations

    def _get_chart_types_for_intent(self, intent: str) -> List[str]:
        """
        Get appropriate chart types for a given intent

        Args:
            intent: Query intent

        Returns:
            List of appropriate chart types
        """
        return self.chart_types.get(intent, ["line_chart", "bar_chart"])

    def _create_visualization_config(self, chart_type: str, intent: str, data_context: Dict[str, Any], index: int) -> Dict[str, Any]:
        """
        Create visualization configuration

        Args:
            chart_type: Type of chart
            intent: Query intent
            data_context: Data context
            index: Visualization index

        Returns:
            Visualization configuration
        """
        data_type = data_context.get("data_type", "mock_data")

        config = {
            "id": f"viz_{index}",
            "type": chart_type,
            "title": self._generate_chart_title(chart_type, intent, index),
            "description": self._generate_chart_description(chart_type, intent),
            "data_source": data_type,
            "config": self._get_chart_config(chart_type, data_context),
            "created_at": datetime.now().isoformat()
        }

        return config

    def _generate_chart_title(self, chart_type: str, intent: str, index: int) -> str:
        """
        Generate chart title based on type and intent

        Args:
            chart_type: Type of chart
            intent: Query intent
            index: Chart index

        Returns:
            Chart title
        """
        intent_title = intent.replace("_", " ").title()
        chart_title = chart_type.replace("_", " ").title()

        return f"{intent_title} - {chart_title}"

    def _generate_chart_description(self, chart_type: str, intent: str) -> str:
        """
        Generate chart description

        Args:
            chart_type: Type of chart
            intent: Query intent

        Returns:
            Chart description
        """
        descriptions = {
            "line_chart": "Shows trends over time",
            "bar_chart": "Compares different categories",
            "area_chart": "Displays cumulative data over time",
            "pie_chart": "Shows proportions of a whole",
            "scatter_plot": "Reveals relationships between variables",
            "histogram": "Shows data distribution",
            "box_plot": "Displays data spread and outliers",
            "heatmap": "Shows correlation patterns",
            "bubble_chart": "Displays three dimensions of data",
            "funnel_chart": "Shows process flow and conversion",
            "tree_map": "Displays hierarchical data structure"
        }

        return descriptions.get(chart_type, "Data visualization")

    def _get_chart_config(self, chart_type: str, data_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get chart-specific configuration

        Args:
            chart_type: Type of chart
            data_context: Data context

        Returns:
            Chart configuration
        """
        base_config = {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {"display": True},
                "tooltip": {"enabled": True}
            }
        }

        # Add chart-specific configurations
        if chart_type == "line_chart":
            base_config.update({
                "scales": {
                    "x": {"type": "time", "time": {"unit": "day"}},
                    "y": {"beginAtZero": True}
                }
            })
        elif chart_type == "bar_chart":
            base_config.update({
                "scales": {
                    "x": {"beginAtZero": True},
                    "y": {"beginAtZero": True}
                }
            })
        elif chart_type == "pie_chart":
            base_config.update({
                "plugins": {
                    "legend": {"position": "bottom"},
                    "tooltip": {"callbacks": {"label": "function(context) { return context.label + ': ' + context.parsed + '%'; }"}}
                }
            })

        return base_config

    def get_visualization_suggestions(self, query_text: str) -> List[str]:
        """
        Get visualization suggestions based on query text

        Args:
            query_text: Natural language query

        Returns:
            List of suggested visualization types
        """
        text_lower = query_text.lower()
        suggestions = []

        if any(word in text_lower for word in ['trend', 'over time', 'history']):
            suggestions.extend(['line_chart', 'area_chart'])

        if any(word in text_lower for word in ['compare', 'vs', 'versus', 'difference']):
            suggestions.extend(['bar_chart', 'column_chart', 'pie_chart'])

        if any(word in text_lower for word in ['distribution', 'spread', 'range']):
            suggestions.extend(['histogram', 'box_plot'])

        if any(word in text_lower for word in ['correlation', 'relationship', 'connection']):
            suggestions.extend(['scatter_plot', 'heatmap'])

        if any(word in text_lower for word in ['predict', 'forecast', 'future']):
            suggestions.extend(['line_chart', 'area_chart'])

        # Remove duplicates and return
        return list(set(suggestions))[:3]  # Limit to 3 suggestions
