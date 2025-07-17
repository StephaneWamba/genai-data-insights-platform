#!/usr/bin/env python3
"""
Comprehensive API Endpoint Testing Script
Tests all endpoints with correct API paths
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def test_endpoint(method: str, url: str, data: Dict[str, Any] = None, expected_status: int = 200) -> bool:
    """Test a single endpoint"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return False

        if response.status_code == expected_status:
            print(f"✅ {method} {url} - Status: {response.status_code}")
            if response.content:
                try:
                    result = response.json()
                    print(
                        f"   Response: {json.dumps(result, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            return True
        else:
            print(
                f"❌ {method} {url} - Expected: {expected_status}, Got: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {url} - Connection Error (Backend not running?)")
        return False
    except Exception as e:
        print(f"❌ {method} {url} - Error: {str(e)}")
        return False


def main():
    """Run all API endpoint tests"""
    print("🚀 Starting API Endpoint Tests")
    print("=" * 50)

    # Test basic health endpoints
    print("\n📋 Testing Health Endpoints:")
    test_endpoint("GET", f"{BASE_URL}/health")
    test_endpoint("GET", f"{BASE_URL}/")

    # Test data endpoints
    print("\n📊 Testing Data Endpoints:")
    test_endpoint("GET", f"{BASE_URL}/api/v1/data/sales")
    test_endpoint("GET", f"{BASE_URL}/api/v1/data/inventory")
    test_endpoint("GET", f"{BASE_URL}/api/v1/data/customers")
    test_endpoint("GET", f"{BASE_URL}/api/v1/data/metrics")
    test_endpoint("GET", f"{BASE_URL}/api/v1/data/search?query=sales")
    test_endpoint("GET", f"{BASE_URL}/api/v1/data/health")

    # Test user endpoints
    print("\n👥 Testing User Endpoints:")
    test_endpoint("GET", f"{BASE_URL}/api/v1/users/health")
    test_endpoint("GET", f"{BASE_URL}/api/v1/users/")

    # Test user creation
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "role": "analyst"
    }
    test_endpoint("POST", f"{BASE_URL}/api/v1/users/", user_data, 201)

    # Test query endpoints
    print("\n🔍 Testing Query Endpoints:")
    test_endpoint("GET", f"{BASE_URL}/api/v1/queries/health")


    # Test query processing
query_data = {
    "query_text": "What are our top selling products?",
    "user_id": "user1"
}
test_endpoint("POST", f"{BASE_URL}/api/v1/queries/process", query_data)

# Test insight endpoints
print("\n💡 Testing Insight Endpoints:")
test_endpoint("GET", f"{BASE_URL}/api/v1/insights/health")

# Test with specific IDs (these might fail if no data exists, which is expected)
print("\n🔍 Testing Specific ID Endpoints (may fail if no data):")
test_endpoint("GET", f"{BASE_URL}/api/v1/queries/1", expected_status=404)
test_endpoint("GET", f"{BASE_URL}/api/v1/users/1", expected_status=404)
test_endpoint("GET", f"{BASE_URL}/api/v1/insights/1", expected_status=404)

print("\n" + "=" * 50)
print("🎯 API Testing Complete!")
print("\nNote: 404 errors for specific IDs are expected if no data exists in the database.")


if __name__ == "__main__":
    main()
