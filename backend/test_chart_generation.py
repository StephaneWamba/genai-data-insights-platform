#!/usr/bin/env python3
"""
Test script for chart generation service
"""

import logging
from app.infrastructure.services.chart_generation_service import ChartGenerationService
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Set up logging
logging.basicConfig(level=logging.INFO)


def test_chart_generation():
    """Test the chart generation service with sample data"""

    # Sample data similar to what we get from ClickHouse
    sample_data = {
        "success": True,
        "rows": [
            {"product": "Bags", "total_revenue": 578207.85},
            {"product": "Smartphones", "total_revenue": 555122.20},
            {"product": "Jewelry", "total_revenue": 544920.60},
            {"product": "Laptops", "total_revenue": 530525.80},
            {"product": "Shoes", "total_revenue": 518636.78}
        ],
        "columns": ["product", "total_revenue"],
        "row_count": 5
    }

    print("Testing chart generation service...")

    # Initialize the service
    chart_service = ChartGenerationService()

    # Test bar chart generation
    print("\n1. Testing bar chart generation...")
    try:
        bar_chart = chart_service.generate_chart_from_query_result(
            sample_data, "bar_chart")
        if "error" in bar_chart:
            print(f"❌ Bar chart failed: {bar_chart['error']}")
        else:
            print(f"✅ Bar chart created successfully!")
            print(f"   Type: {bar_chart.get('type')}")
            print(f"   Title: {bar_chart.get('title')}")
            print(f"   Data points: {bar_chart.get('data_points')}")
            print(f"   Image length: {len(bar_chart.get('image', ''))}")
    except Exception as e:
        print(f"❌ Bar chart exception: {e}")

    # Test pie chart generation
    print("\n2. Testing pie chart generation...")
    try:
        pie_chart = chart_service.generate_chart_from_query_result(
            sample_data, "pie_chart")
        if "error" in pie_chart:
            print(f"❌ Pie chart failed: {pie_chart['error']}")
        else:
            print(f"✅ Pie chart created successfully!")
            print(f"   Type: {pie_chart.get('type')}")
            print(f"   Title: {pie_chart.get('title')}")
            print(f"   Data points: {pie_chart.get('data_points')}")
            print(f"   Image length: {len(pie_chart.get('image', ''))}")
    except Exception as e:
        print(f"❌ Pie chart exception: {e}")

    # Test line chart generation
    print("\n3. Testing line chart generation...")
    try:
        line_chart = chart_service.generate_chart_from_query_result(
            sample_data, "line_chart")
        if "error" in line_chart:
            print(f"❌ Line chart failed: {line_chart['error']}")
        else:
            print(f"✅ Line chart created successfully!")
            print(f"   Type: {line_chart.get('type')}")
            print(f"   Title: {line_chart.get('title')}")
            print(f"   Data points: {line_chart.get('data_points')}")
            print(f"   Image length: {len(line_chart.get('image', ''))}")
    except Exception as e:
        print(f"❌ Line chart exception: {e}")


if __name__ == "__main__":
    test_chart_generation()
