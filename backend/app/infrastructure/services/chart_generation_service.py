import logging
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
from datetime import datetime
import numpy as np

logger = logging.getLogger("chart_generation_service")

# Centralized column label mapping
COLUMN_LABELS = {
    'p': 'Product',
    's': 'Store',
    't': 'Total Revenue',
    'r': 'Revenue',
    'q': 'Quantity',
    'd': 'Date',
    'c': 'Category'
}


class ChartGenerationService:
    """
    Service for preparing raw chart data for frontend visualization.
    Prepares data in formats suitable for frontend charting libraries.
    """

    def __init__(self):
        pass

    def generate_chart_data_from_query_result(self, query_result: Dict[str, Any], chart_type: str) -> Dict[str, Any]:
        try:
            if not query_result.get("success"):
                return {"error": "Query result is not successful"}
            rows = query_result.get("rows", [])
            columns = query_result.get("columns", [])
            if not rows or not columns:
                return {"error": "No data available for chart generation"}
            df = pd.DataFrame(rows)
            if chart_type == "bar_chart":
                return self._prepare_bar_chart_data(df, columns)
            elif chart_type == "line_chart":
                return self._prepare_line_chart_data(df, columns)
            elif chart_type == "pie_chart":
                return self._prepare_pie_chart_data(df, columns)
            elif chart_type == "scatter_plot":
                return self._prepare_scatter_plot_data(df, columns)
            elif chart_type == "area_chart":
                return self._prepare_area_chart_data(df, columns)
            elif chart_type == "doughnut_chart":
                return self._prepare_doughnut_chart_data(df, columns)
            elif chart_type == "horizontal_bar_chart":
                return self._prepare_horizontal_bar_chart_data(df, columns)
            elif chart_type == "bubble_chart":
                return self._prepare_bubble_chart_data(df, columns)
            elif chart_type == "radar_chart":
                return self._prepare_radar_chart_data(df, columns)
            elif chart_type == "stacked_bar_chart":
                return self._prepare_stacked_bar_chart_data(df, columns)
            elif chart_type == "multi_line_chart":
                return self._prepare_multi_line_chart_data(df, columns)
            else:
                return self._prepare_bar_chart_data(df, columns)
        except Exception as e:
            logger.error(f"Error preparing chart data: {e}", exc_info=True)
            return {"error": f"Chart data preparation failed: {str(e)}"}

    def _prepare_bar_chart_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        x_col, y_col = self._identify_chart_columns(df, columns, "bar")
        if not x_col or not y_col:
            return {"error": "Cannot identify suitable columns for bar chart"}

        # Convert y column to numeric if it's a string
        if df[y_col].dtype == 'object' or df[y_col].dtype == 'string':
            try:
                # Remove any non-numeric characters except dots and minus signs
                numeric_values = df[y_col].astype(
                    str).str.replace(r'[^\d.-]', '', regex=True)
                # Convert to float
                df[y_col] = pd.to_numeric(numeric_values, errors='coerce')
                # Handle inf, -inf, and NaN values
                df[y_col] = df[y_col].replace(
                    [np.inf, -np.inf], np.nan)
                df[y_col] = df[y_col].fillna(0)  # Replace NaN with 0
            except Exception as e:
                logger.warning(
                    f"Bar chart - Failed to convert {y_col} to numeric: {e}")
                return {"error": f"Cannot convert {y_col} to numeric values"}

        x_label = COLUMN_LABELS.get(x_col, x_col.title())
        y_label = COLUMN_LABELS.get(y_col, y_col.title())
        chart_data = {
            "type": "bar",
            "data": {
                "labels": df[x_col].astype(str).tolist(),
                "datasets": [{
                    "label": y_label,
                    "data": df[y_col].tolist(),
                    "backgroundColor": "rgba(54, 162, 235, 0.7)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": f"{y_label} by {x_label}"
                    },
                    "legend": {"display": True}
                },
                "scales": {
                    "y": {"beginAtZero": True, "title": {"display": True, "text": y_label}},
                    "x": {"title": {"display": True, "text": x_label}}
                }
            }
        }
        return {
            "type": "bar_chart",
            "title": f"{y_label} by {x_label}",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [x_col, y_col],
            "data_source": "sales_data"
        }

    def _prepare_line_chart_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        x_col, y_col = self._identify_chart_columns(df, columns, "line")
        if not x_col or not y_col:
            return {"error": "Cannot identify suitable columns for line chart"}

        # Convert y column to numeric if it's a string
        if df[y_col].dtype == 'object' or df[y_col].dtype == 'string':
            try:
                # Remove any non-numeric characters except dots and minus signs
                numeric_values = df[y_col].astype(
                    str).str.replace(r'[^\d.-]', '', regex=True)
                # Convert to float
                df[y_col] = pd.to_numeric(numeric_values, errors='coerce')
                # Handle inf, -inf, and NaN values
                df[y_col] = df[y_col].replace(
                    [np.inf, -np.inf], np.nan)
                df[y_col] = df[y_col].fillna(0)  # Replace NaN with 0
            except Exception as e:
                logger.warning(
                    f"Line chart - Failed to convert {y_col} to numeric: {e}")
                return {"error": f"Cannot convert {y_col} to numeric values"}

        x_label = COLUMN_LABELS.get(x_col, x_col.title())
        y_label = COLUMN_LABELS.get(y_col, y_col.title())
        df_sorted = df.sort_values(x_col)
        chart_data = {
            "type": "line",
            "data": {
                "labels": df_sorted[x_col].astype(str).tolist(),
                "datasets": [{
                    "label": y_label,
                    "data": df_sorted[y_col].tolist(),
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "borderWidth": 2,
                    "fill": False,
                    "tension": 0.1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {"display": True, "text": f"{y_label} Trend over {x_label}"},
                    "legend": {"display": True}
                },
                "scales": {
                    "y": {"beginAtZero": True, "title": {"display": True, "text": y_label}},
                    "x": {"title": {"display": True, "text": x_label}}
                }
            }
        }
        return {
            "type": "line_chart",
            "title": f"{y_label} Trend over {x_label}",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [x_col, y_col],
            "data_source": "sales_data"
        }

    def _prepare_pie_chart_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        category_col, value_col = self._identify_chart_columns(
            df, columns, "pie")
        if not category_col or not value_col:
            return {"error": "Cannot identify suitable columns for pie chart"}

        # Convert value column to numeric if it's a string
        if df[value_col].dtype == 'object' or df[value_col].dtype == 'string':
            try:
                # Remove any non-numeric characters except dots and minus signs
                numeric_values = df[value_col].astype(
                    str).str.replace(r'[^\d.-]', '', regex=True)
                # Convert to float
                df[value_col] = pd.to_numeric(numeric_values, errors='coerce')
                # Handle inf, -inf, and NaN values
                df[value_col] = df[value_col].replace(
                    [np.inf, -np.inf], np.nan)
                df[value_col] = df[value_col].fillna(0)  # Replace NaN with 0
            except Exception as e:
                logger.warning(
                    f"Pie chart - Failed to convert {value_col} to numeric: {e}")
                return {"error": f"Cannot convert {value_col} to numeric values"}

        category_label = COLUMN_LABELS.get(category_col, category_col.title())
        value_label = COLUMN_LABELS.get(value_col, value_col.title())
        chart_data = {
            "type": "pie",
            "data": {
                "labels": df[category_col].astype(str).tolist(),
                "datasets": [{
                    "data": df[value_col].tolist(),
                    "backgroundColor": [
                        "rgba(255, 99, 132, 0.7)",
                        "rgba(54, 162, 235, 0.7)",
                        "rgba(255, 205, 86, 0.7)",
                        "rgba(75, 192, 192, 0.7)",
                        "rgba(153, 102, 255, 0.7)",
                        "rgba(255, 159, 64, 0.7)"
                    ],
                    "borderColor": [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 205, 86, 1)",
                        "rgba(75, 192, 192, 1)",
                        "rgba(153, 102, 255, 1)",
                        "rgba(255, 159, 64, 1)"
                    ],
                    "borderWidth": 1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {"display": True, "text": f"Distribution of {value_label} by {category_label}"},
                    "legend": {"display": True, "position": "bottom"}
                }
            }
        }
        return {
            "type": "pie_chart",
            "title": f"Distribution of {value_label} by {category_label}",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [category_col, value_col],
            "data_source": "sales_data"
        }

    def _prepare_scatter_plot_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        x_col, y_col = self._identify_chart_columns(df, columns, "scatter")
        if not x_col or not y_col:
            return {"error": "Cannot identify suitable columns for scatter plot"}
        x_label = COLUMN_LABELS.get(x_col, x_col.title())
        y_label = COLUMN_LABELS.get(y_col, y_col.title())
        chart_data = {
            "type": "scatter",
            "data": {
                "datasets": [{
                    "label": f"{y_label} vs {x_label}",
                    "data": [
                        {"x": x, "y": y} for x, y in zip(df[x_col], df[y_col])
                    ],
                    "backgroundColor": "rgba(255, 99, 132, 0.7)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {"display": True, "text": f"{y_label} vs {x_label}"},
                    "legend": {"display": True}
                },
                "scales": {
                    "y": {"beginAtZero": True, "title": {"display": True, "text": y_label}},
                    "x": {"beginAtZero": True, "title": {"display": True, "text": x_label}}
                }
            }
        }
        return {
            "type": "scatter_plot",
            "title": f"{y_label} vs {x_label}",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [x_col, y_col],
            "data_source": "sales_data"
        }

    def _prepare_area_chart_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        x_col, y_col = self._identify_chart_columns(df, columns, "area")
        if not x_col or not y_col:
            return {"error": "Cannot identify suitable columns for area chart"}
        x_label = COLUMN_LABELS.get(x_col, x_col.title())
        y_label = COLUMN_LABELS.get(y_col, y_col.title())
        df_sorted = df.sort_values(x_col)
        chart_data = {
            "type": "line",
            "data": {
                "labels": df_sorted[x_col].astype(str).tolist(),
                "datasets": [{
                    "label": y_label,
                    "data": df_sorted[y_col].tolist(),
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "backgroundColor": "rgba(75, 192, 192, 0.3)",
                    "borderWidth": 2,
                    "fill": True,
                    "tension": 0.1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {"display": True, "text": f"{y_label} Area Chart over {x_label}"},
                    "legend": {"display": True}
                },
                "scales": {
                    "y": {"beginAtZero": True, "title": {"display": True, "text": y_label}},
                    "x": {"title": {"display": True, "text": x_label}}
                }
            }
        }
        return {
            "type": "area_chart",
            "title": f"{y_label} Area Chart over {x_label}",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [x_col, y_col],
            "data_source": "sales_data"
        }

    def _identify_chart_columns(self, df: pd.DataFrame, columns: List[str], chart_type: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            if chart_type in ["bar", "line", "area"]:
                x_col = None
                y_col = None
                for col in columns:
                    if df[col].dtype == 'object' or df[col].dtype == 'string':
                        sample_values = df[col].dropna().head(10).astype(str)
                        if len(sample_values) > 0:
                            numeric_count = sum(1 for v in sample_values if str(
                                v).replace('.', '').replace('-', '').isdigit())
                            if numeric_count < len(sample_values) * 0.5:
                                x_col = col
                            elif numeric_count == len(sample_values):
                                y_col = col
                    elif df[col].dtype in ['int64', 'float64']:
                        y_col = col
                if not x_col and not y_col:
                    if len(columns) >= 2:
                        x_col = columns[0]
                        y_col = columns[1]
                elif not x_col:
                    for col in columns:
                        if col != y_col:
                            x_col = col
                            break
                elif not y_col:
                    for col in columns:
                        if col != x_col:
                            y_col = col
                            break
                return x_col, y_col
            elif chart_type == "pie":
                category_col = None
                value_col = None

                # First pass: look for actual numeric columns
                for col in columns:
                    if df[col].dtype in ['int64', 'float64']:
                        value_col = col
                    elif df[col].dtype == 'object' or df[col].dtype == 'string':
                        category_col = col

                # Special handling for known column patterns from dynamic queries
                if len(columns) == 2:
                    col1, col2 = columns[0], columns[1]

                    # Check if we have the common pattern: 't' (total) and 's' (store)
                    if col1 == 't' and col2 == 's':
                        # 't' is total revenue (numeric), 's' is store (categorical)
                        value_col = 't'
                        category_col = 's'
                        logger.info(
                            "Pie chart - Detected 't' (total) and 's' (store) pattern")
                    elif col1 == 's' and col2 == 't':
                        # 's' is store (categorical), 't' is total revenue (numeric)
                        category_col = 's'
                        value_col = 't'
                        logger.info(
                            "Pie chart - Detected 's' (store) and 't' (total) pattern")
                    else:
                        # Try to determine which is numeric and which is categorical
                        col1_numeric = False
                        col2_numeric = False

                        try:
                            col1_test = pd.to_numeric(df[col1].astype(str).str.replace(
                                r'[^\d.-]', '', regex=True), errors='coerce')
                            col1_numeric = not col1_test.isna().all()
                        except:
                            pass

                        try:
                            col2_test = pd.to_numeric(df[col2].astype(str).str.replace(
                                r'[^\d.-]', '', regex=True), errors='coerce')
                            col2_numeric = not col2_test.isna().all()
                        except:
                            pass

                        # If both are numeric, use first as category, second as value
                        if col1_numeric and col2_numeric:
                            category_col = col1
                            value_col = col2
                            logger.info(
                                f"Pie chart - Both columns numeric, using {category_col} as category, {value_col} as value")
                        elif col1_numeric and not col2_numeric:
                            value_col = col1
                            category_col = col2
                            logger.info(
                                f"Pie chart - First numeric, second categorical: {value_col} -> {category_col}")
                        elif not col1_numeric and col2_numeric:
                            category_col = col1
                            value_col = col2
                            logger.info(
                                f"Pie chart - First categorical, second numeric: {category_col} -> {value_col}")
                        else:
                            # Both appear to be categorical, use first as category, second as value
                            category_col = col1
                            value_col = col2
                            logger.info(
                                f"Pie chart - Both categorical, using {category_col} as category, {value_col} as value")

                # Fallback: if no columns identified, use first as category, second as value
                if not category_col and not value_col and len(columns) >= 2:
                    category_col = columns[0]
                    value_col = columns[1]
                    logger.info(
                        f"Pie chart - Fallback: using {category_col} as category, {value_col} as value")
                elif not value_col and category_col:
                    # If we have a category but no value, use the other column
                    for col in columns:
                        if col != category_col:
                            value_col = col
                            break

                return category_col, value_col
            elif chart_type == "scatter":
                numeric_cols = []
                for col in columns:
                    if df[col].dtype in ['int64', 'float64']:
                        numeric_cols.append(col)
                if len(numeric_cols) >= 2:
                    return numeric_cols[0], numeric_cols[1]
                elif len(columns) >= 2:
                    return columns[0], columns[1]
            return None, None
        except Exception as e:
            logger.error(f"Error identifying chart columns: {e}")
            return None, None

    def _prepare_doughnut_chart_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        category_col, value_col = self._identify_chart_columns(
            df, columns, "pie")

        if not category_col or not value_col:
            return {"error": "Cannot identify suitable columns for doughnut chart"}

        # Convert value column to numeric if it's a string
        if df[value_col].dtype == 'object' or df[value_col].dtype == 'string':
            try:
                # Remove any non-numeric characters except dots and minus signs
                numeric_values = df[value_col].astype(
                    str).str.replace(r'[^\d.-]', '', regex=True)
                # Convert to float
                df[value_col] = pd.to_numeric(numeric_values, errors='coerce')

                # Handle inf, -inf, and NaN values
                df[value_col] = df[value_col].replace(
                    [np.inf, -np.inf], np.nan)
                df[value_col] = df[value_col].fillna(0)  # Replace NaN with 0

            except Exception as e:
                logger.warning(
                    f"Doughnut chart - Failed to convert {value_col} to numeric: {e}")
                return {"error": f"Cannot convert {value_col} to numeric values"}

        category_label = COLUMN_LABELS.get(category_col, category_col.title())
        value_label = COLUMN_LABELS.get(value_col, value_col.title())
        chart_data = {
            "type": "doughnut",
            "data": {
                "labels": df[category_col].astype(str).tolist(),
                "datasets": [{
                    "data": df[value_col].tolist(),
                    "backgroundColor": [
                        "rgba(255, 99, 132, 0.8)",
                        "rgba(54, 162, 235, 0.8)",
                        "rgba(255, 205, 86, 0.8)",
                        "rgba(75, 192, 192, 0.8)",
                        "rgba(153, 102, 255, 0.8)",
                        "rgba(255, 159, 64, 0.8)"
                    ],
                    "borderColor": [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 205, 86, 1)",
                        "rgba(75, 192, 192, 1)",
                        "rgba(153, 102, 255, 1)",
                        "rgba(255, 159, 64, 1)"
                    ],
                    "borderWidth": 2
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {"display": True, "text": f"Distribution of {value_label} by {category_label}"},
                    "legend": {"display": True, "position": "bottom"}
                }
            }
        }
        return {
            "type": "doughnut_chart",
            "title": f"Distribution of {value_label} by {category_label}",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [category_col, value_col],
            "data_source": "sales_data"
        }

    def _prepare_horizontal_bar_chart_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        x_col, y_col = self._identify_chart_columns(df, columns, "bar")
        if not x_col or not y_col:
            return {"error": "Cannot identify suitable columns for horizontal bar chart"}

        # Convert y column to numeric if it's a string
        if df[y_col].dtype == 'object' or df[y_col].dtype == 'string':
            try:
                # Remove any non-numeric characters except dots and minus signs
                numeric_values = df[y_col].astype(
                    str).str.replace(r'[^\d.-]', '', regex=True)
                # Convert to float
                df[y_col] = pd.to_numeric(numeric_values, errors='coerce')
                # Handle inf, -inf, and NaN values
                df[y_col] = df[y_col].replace(
                    [np.inf, -np.inf], np.nan)
                df[y_col] = df[y_col].fillna(0)  # Replace NaN with 0
            except Exception as e:
                logger.warning(
                    f"Horizontal bar chart - Failed to convert {y_col} to numeric: {e}")
                return {"error": f"Cannot convert {y_col} to numeric values"}

        x_label = COLUMN_LABELS.get(x_col, x_col.title())
        y_label = COLUMN_LABELS.get(y_col, y_col.title())
        chart_data = {
            "type": "bar",
            "data": {
                "labels": df[x_col].astype(str).tolist(),
                "datasets": [{
                    "label": y_label,
                    "data": df[y_col].tolist(),
                    "backgroundColor": "rgba(75, 192, 192, 0.7)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 1
                }]
            },
            "options": {
                "indexAxis": "y",
                "responsive": True,
                "plugins": {
                    "title": {"display": True, "text": f"{y_label} by {x_label}"},
                    "legend": {"display": True}
                },
                "scales": {
                    "x": {"beginAtZero": True, "title": {"display": True, "text": y_label}},
                    "y": {"title": {"display": True, "text": x_label}}
                }
            }
        }
        return {
            "type": "horizontal_bar_chart",
            "title": f"{y_label} by {x_label}",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [x_col, y_col],
            "data_source": "sales_data"
        }

    def _prepare_bubble_chart_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        # For bubble chart, we need 3 numeric columns: x, y, and radius
        numeric_cols = [
            col for col in columns if df[col].dtype in ['int64', 'float64']]
        if len(numeric_cols) < 3:
            return {"error": "Bubble chart requires at least 3 numeric columns"}

        x_col, y_col, r_col = numeric_cols[0], numeric_cols[1], numeric_cols[2]
        x_label = COLUMN_LABELS.get(x_col, x_col.title())
        y_label = COLUMN_LABELS.get(y_col, y_col.title())
        r_label = COLUMN_LABELS.get(r_col, r_col.title())

        chart_data = {
            "type": "bubble",
            "data": {
                "datasets": [{
                    "label": f"{y_label} vs {x_label}",
                    "data": [
                        {"x": x, "y": y, "r": r} for x, y, r in zip(df[x_col], df[y_col], df[r_col])
                    ],
                    "backgroundColor": "rgba(255, 99, 132, 0.6)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {"display": True, "text": f"{y_label} vs {x_label} (Size: {r_label})"},
                    "legend": {"display": True}
                },
                "scales": {
                    "y": {"beginAtZero": True, "title": {"display": True, "text": y_label}},
                    "x": {"beginAtZero": True, "title": {"display": True, "text": x_label}}
                }
            }
        }
        return {
            "type": "bubble_chart",
            "title": f"{y_label} vs {x_label} (Size: {r_label})",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [x_col, y_col, r_col],
            "data_source": "sales_data"
        }

    def _prepare_radar_chart_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        # For radar chart, we need categorical labels and numeric values
        category_col, value_col = self._identify_chart_columns(
            df, columns, "pie")
        if not category_col or not value_col:
            return {"error": "Cannot identify suitable columns for radar chart"}

        # Convert value column to numeric if it's a string
        if df[value_col].dtype == 'object' or df[value_col].dtype == 'string':
            try:
                # Remove any non-numeric characters except dots and minus signs
                numeric_values = df[value_col].astype(
                    str).str.replace(r'[^\d.-]', '', regex=True)
                # Convert to float
                df[value_col] = pd.to_numeric(numeric_values, errors='coerce')

                # Handle inf, -inf, and NaN values
                df[value_col] = df[value_col].replace(
                    [np.inf, -np.inf], np.nan)
                df[value_col] = df[value_col].fillna(0)  # Replace NaN with 0

                logger.info(
                    f"Radar chart - Converted {value_col} to numeric values")
            except Exception as e:
                logger.warning(
                    f"Radar chart - Failed to convert {value_col} to numeric: {e}")
                return {"error": f"Cannot convert {value_col} to numeric values"}

        category_label = COLUMN_LABELS.get(category_col, category_col.title())
        value_label = COLUMN_LABELS.get(value_col, value_col.title())

        chart_data = {
            "type": "radar",
            "data": {
                "labels": df[category_col].astype(str).tolist(),
                "datasets": [{
                    "label": value_label,
                    "data": df[value_col].tolist(),
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 2,
                    "pointBackgroundColor": "rgba(54, 162, 235, 1)",
                    "pointBorderColor": "#fff",
                    "pointHoverBackgroundColor": "#fff",
                    "pointHoverBorderColor": "rgba(54, 162, 235, 1)"
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {"display": True, "text": f"{value_label} by {category_label}"},
                    "legend": {"display": True}
                },
                "scales": {
                    "r": {
                        "beginAtZero": True,
                        "title": {"display": True, "text": value_label}
                    }
                }
            }
        }
        return {
            "type": "radar_chart",
            "title": f"{value_label} by {category_label}",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [category_col, value_col],
            "data_source": "sales_data"
        }

    def _prepare_stacked_bar_chart_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        # For stacked bar, we'll use the same data as regular bar but with stacking enabled
        x_col, y_col = self._identify_chart_columns(df, columns, "bar")
        if not x_col or not y_col:
            return {"error": "Cannot identify suitable columns for stacked bar chart"}

        x_label = COLUMN_LABELS.get(x_col, x_col.title())
        y_label = COLUMN_LABELS.get(y_col, y_col.title())

        chart_data = {
            "type": "bar",
            "data": {
                "labels": df[x_col].astype(str).tolist(),
                "datasets": [{
                    "label": y_label,
                    "data": df[y_col].tolist(),
                    "backgroundColor": "rgba(255, 99, 132, 0.7)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1,
                    "stack": "Stack 0"
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {"display": True, "text": f"{y_label} by {x_label} (Stacked)"},
                    "legend": {"display": True}
                },
                "scales": {
                    "x": {"stacked": True, "title": {"display": True, "text": x_label}},
                    "y": {"stacked": True, "beginAtZero": True, "title": {"display": True, "text": y_label}}
                }
            }
        }
        return {
            "type": "stacked_bar_chart",
            "title": f"{y_label} by {x_label} (Stacked)",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [x_col, y_col],
            "data_source": "sales_data"
        }

    def _prepare_multi_line_chart_data(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        # For multi-line, we'll create multiple datasets if we have multiple numeric columns
        numeric_cols = [
            col for col in columns if df[col].dtype in ['int64', 'float64']]
        categorical_cols = [
            col for col in columns if df[col].dtype in ['object', 'string']]

        if len(numeric_cols) < 2 or len(categorical_cols) < 1:
            return {"error": "Multi-line chart requires at least 2 numeric columns and 1 categorical column"}

        x_col = categorical_cols[0]
        x_label = COLUMN_LABELS.get(x_col, x_col.title())

        # Create datasets for each numeric column
        datasets = []
        colors = [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 205, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)"
        ]

        # Limit to 3 lines for readability
        for i, col in enumerate(numeric_cols[:3]):
            y_label = COLUMN_LABELS.get(col, col.title())
            datasets.append({
                "label": y_label,
                "data": df[col].tolist(),
                "borderColor": colors[i % len(colors)],
                "backgroundColor": colors[i % len(colors)].replace("1)", "0.2)"),
                "borderWidth": 2,
                "fill": False,
                "tension": 0.1
            })

        chart_data = {
            "type": "line",
            "data": {
                "labels": df[x_col].astype(str).tolist(),
                "datasets": datasets
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {"display": True, "text": f"Multiple Metrics over {x_label}"},
                    "legend": {"display": True}
                },
                "scales": {
                    "y": {"beginAtZero": True, "title": {"display": True, "text": "Value"}},
                    "x": {"title": {"display": True, "text": x_label}}
                }
            }
        }
        return {
            "type": "multi_line_chart",
            "title": f"Multiple Metrics over {x_label}",
            "chart_data": chart_data,
            "data_points": len(df),
            "columns_used": [x_col] + numeric_cols[:3],
            "data_source": "sales_data"
        }
