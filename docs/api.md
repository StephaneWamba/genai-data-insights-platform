# API Reference

Complete API documentation for the GenAI Data Insights Platform.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API uses simple user identification via `user_id` parameter. For production, implement proper JWT authentication.

## Core Endpoints

### 1. Natural Language Query Processing

**Transform business questions into AI-powered insights.**

#### POST `/api/v1/queries/process`

Process natural language queries and return actionable insights.

**Request:**

```json
{
  "query_text": "Why are shoe sales down in Paris stores this quarter?",
  "user_id": "user123"
}
```

**Response:**

```json
{
  "success": true,
  "query": {
    "id": 18,
    "text": "Why are shoe sales down in Paris stores this quarter?",
    "user_id": "user123",
    "processed": true,
    "created_at": "2025-07-17T14:26:25.050752"
  },
  "intent": {
    "intent": "root_cause",
    "confidence": 0.9,
    "categories": ["sales", "store_performance"],
    "data_sources": ["sales_data", "store_data"]
  },
  "insights": [
    {
      "title": "Shift in Consumer Preferences",
      "description": "Analysis shows changing customer behavior towards online shopping. Consider investing in omnichannel strategy.",
      "category": "trend",
      "confidence_score": 0.8,
      "data_sources": ["clickhouse_sales_data"]
    },
    {
      "title": "Competitive Pricing Strategy",
      "description": "Competitors in Paris have aggressive pricing. Revisit pricing strategy to stay competitive.",
      "category": "recommendation",
      "confidence_score": 0.7,
      "data_sources": ["clickhouse_sales_data"]
    }
  ],
  "recommendations": [
    "Monitor trend continuation",
    "Consider implementing suggested actions"
  ],
  "visualizations": [
    {
      "type": "bar_chart",
      "title": "Root_Cause Visualization",
      "data_source": "sales_data"
    }
  ],
  "processed_at": "2025-07-17T14:26:47.861234"
}
```

**Example Queries:**

- "What products are selling best in Paris this month?"
- "Show me inventory levels for electronics across all stores"
- "What's causing the spike in returns for clothing items?"
- "Which stores have the highest profit margins?"

---

### 2. Real-Time Data Endpoints

#### GET `/api/v1/data/sales`

Retrieve real-time sales data from ClickHouse.

**Parameters:**

- `days` (optional): Number of days of data (default: 30)

**Response:**

```json
{
  "data_type": "sales",
  "days": 30,
  "records": 1944,
  "data": [
    {
      "date": "2025-07-16",
      "product": "Tablets",
      "category": "General",
      "store": "Rome South",
      "quantity": 6,
      "revenue": 1237.24,
      "profit": 480.87
    }
  ]
}
```

#### GET `/api/v1/data/inventory`

Get current inventory levels across all stores.

**Response:**

```json
{
  "data_type": "inventory",
  "records": 150,
  "data": [
    {
      "product": "Bags",
      "category": "General",
      "store": "Berlin Central",
      "quantity": 75,
      "reorder_level": 94,
      "supplier": "Supplier_16"
    }
  ]
}
```

#### GET `/api/v1/data/customers`

Retrieve customer data and segments.

**Parameters:**

- `count` (optional): Number of customers (default: 100)

**Response:**

```json
{
  "data_type": "customers",
  "count": 100,
  "data": [
    {
      "customer_id": "CUST_000001",
      "name": "Customer 1",
      "email": "customer1@example.com",
      "segment": "36-45",
      "total_purchases": 23.0,
      "last_purchase_date": "2025-04-03"
    }
  ]
}
```

#### GET `/api/v1/data/metrics`

Get key business performance metrics.

**Response:**

```json
{
  "data_type": "metrics",
  "data": {
    "total_revenue": 150000.0,
    "total_profit": 30000.0,
    "profit_margin": 20.0,
    "total_customers": 1250,
    "average_order_value": 120.0,
    "inventory_turnover": 4.5
  }
}
```

#### GET `/api/v1/data/search`

Search data based on natural language query.

**Parameters:**

- `query` (required): Search query string

**Response:**

```json
{
  "query": "sales trends",
  "data_type": "sales",
  "records": 25,
  "data": [
    {
      "date": "2025-07-15",
      "product": "Running Shoes",
      "revenue": 750.0
    }
  ]
}
```

---

### 3. Health & Monitoring

#### GET `/api/v1/data/health`

Check data service health status.

**Response:**

```json
{
  "service": "real_data",
  "status": "healthy",
  "message": "Real data service is operational",
  "available_data_types": ["sales", "inventory", "customers", "metrics"]
}
```

#### GET `/api/v1/data/cache/health`

Check Redis cache system health.

**Response:**

```json
{
  "service": "cache",
  "status": "healthy",
  "message": "Cache health check completed",
  "statistics": {
    "hits": 150,
    "misses": 25,
    "hit_rate": 0.86
  }
}
```

#### GET `/api/v1/queries/health`

Check query processing service health.

**Response:**

```json
{
  "service": "query_processing",
  "status": "healthy",
  "message": "Query processing service is operational"
}
```

---

## Error Responses

### Validation Error (400)

```json
{
  "detail": [
    {
      "type": "string_type",
      "loc": ["body", "user_id"],
      "msg": "Input should be a valid string",
      "input": 1
    }
  ]
}
```

### Internal Server Error (500)

```json
{
  "detail": "An error occurred while retrieving sales data"
}
```

### Not Found (404)

```json
{
  "detail": "Query not found"
}
```

---

## Rate Limiting

- **Default**: 100 requests per minute per IP
- **Query Processing**: 10 requests per minute per user
- **Data Endpoints**: 1000 requests per minute

---

## Data Sources

All data comes from real ClickHouse tables:

| Endpoint     | ClickHouse Table           | Description                     |
| ------------ | -------------------------- | ------------------------------- |
| `/sales`     | `sales_data`               | Transaction-level sales records |
| `/inventory` | `inventory_data`           | Current stock levels            |
| `/customers` | `customer_data`            | Customer profiles and segments  |
| `/metrics`   | Calculated from sales_data | Aggregated business KPIs        |

---

## Testing Examples

### Test with curl

```bash
# Test natural language query
curl -X POST "http://localhost:8000/api/v1/queries/process" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "What are the top 5 products by revenue this month?",
    "user_id": "test_user"
  }'

# Test data endpoints
curl "http://localhost:8000/api/v1/data/sales?days=7"
curl "http://localhost:8000/api/v1/data/inventory"
curl "http://localhost:8000/api/v1/data/customers?count=10"

# Test health endpoints
curl "http://localhost:8000/api/v1/data/health"
curl "http://localhost:8000/api/v1/data/cache/health"
```

### Test with Python

```python
import requests

# Query processing
response = requests.post(
    "http://localhost:8000/api/v1/queries/process",
    json={
        "query_text": "Show me sales trends for electronics",
        "user_id": "python_test"
    }
)
print(response.json())

# Data retrieval
sales_data = requests.get("http://localhost:8000/api/v1/data/sales")
print(f"Records: {sales_data.json()['records']}")
```

---

## Performance

- **Response Time**: < 2 seconds for complex queries
- **Throughput**: 1000+ requests/minute
- **Caching**: Redis-based with 30-minute TTL
- **Data Freshness**: Real-time from ClickHouse
