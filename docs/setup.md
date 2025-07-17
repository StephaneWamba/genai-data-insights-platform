# Setup Guide

Complete setup instructions for the GenAI Data Insights Platform.

## Prerequisites

- **Docker & Docker Compose** (v2.0+)
- **OpenAI API Key** (GPT-4o Mini access)
- **8GB+ RAM** (for ClickHouse + Redis + FastAPI)

## Quick Setup

### 1. Clone Repository

```bash
git clone https://github.com/StephaneWamba/genai-data-insights-platform.git
cd genai-data-insights-platform
```

### 2. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Start Services

```bash
# Start all services (ClickHouse, Redis, FastAPI, etc.)
docker-compose up -d

# Check service status
docker-compose ps
```

### 4. Verify Installation

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/data/health

# Expected response:
{
  "service": "real_data",
  "status": "healthy",
  "message": "Real data service is operational"
}
```

## Service Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   ClickHouse    │    │     Redis       │
│   (Port 8000)   │◄──►│   (Port 8123)   │    │   (Port 6379)   │
│                 │    │                 │    │                 │
│ - API Endpoints │    │ - Sales Data    │    │ - Query Cache   │
│ - AI Processing │    │ - Inventory     │    │ - Session Data  │
│ - Health Checks │    │ - Customers     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Data Population

The platform comes with realistic sample data:

```bash
# Populate ClickHouse with sample data
python scripts/populate_clickhouse_data.py

# Verify data is loaded
curl http://localhost:8000/api/v1/data/sales | jq '.records'
# Should return: 1944 (or similar number)
```

## Testing the Platform

### Test Natural Language Query

```bash
curl -X POST "http://localhost:8000/api/v1/queries/process" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "What are the top selling products in Paris this month?",
    "user_id": "user123"
  }'
```

### Test Data Endpoints

```bash
# Sales data
curl http://localhost:8000/api/v1/data/sales

# Inventory data
curl http://localhost:8000/api/v1/data/inventory

# Customer data
curl http://localhost:8000/api/v1/data/customers

# Business metrics
curl http://localhost:8000/api/v1/data/metrics
```

## Access Points

| Service               | URL                                          | Purpose              |
| --------------------- | -------------------------------------------- | -------------------- |
| **API Documentation** | http://localhost:8000/docs                   | Interactive API docs |
| **Health Check**      | http://localhost:8000/api/v1/data/health     | Service status       |
| **Sales Data**        | http://localhost:8000/api/v1/data/sales      | Real-time sales      |
| **Query Processing**  | http://localhost:8000/api/v1/queries/process | AI insights          |

## Troubleshooting

### Common Issues

**1. OpenAI API Key Error**

```
Error: OpenAI client not available, using fallback insights
```

**Solution**: Check your `.env` file has the correct `OPENAI_API_KEY`

**2. ClickHouse Connection Failed**

```
Error: Failed to connect to ClickHouse
```

**Solution**:

```bash
docker-compose restart clickhouse
docker-compose logs clickhouse
```

**3. Port Already in Use**

```
Error: Port 8000 is already in use
```

**Solution**:

```bash
# Find process using port 8000
netstat -ano | findstr :8000
# Kill the process or change port in docker-compose.yml
```

**4. Insufficient Memory**

```
Error: ClickHouse container keeps restarting
```

**Solution**: Increase Docker memory limit to 8GB+ in Docker Desktop settings

### Logs and Debugging

```bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs clickhouse
docker-compose logs redis

# Follow logs in real-time
docker-compose logs -f backend
```

### Reset Everything

```bash
# Stop and remove all containers
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Start fresh
docker-compose up -d
```

## Production Deployment

For production deployment, consider:

1. **Environment Variables**: Use proper secrets management
2. **SSL/TLS**: Add HTTPS with reverse proxy (nginx)
3. **Monitoring**: Add Prometheus/Grafana for metrics
4. **Backup**: Configure ClickHouse backups
5. **Scaling**: Use Docker Swarm or Kubernetes

## Performance Tuning

- **ClickHouse**: Adjust memory settings for your data size
- **Redis**: Configure persistence and memory limits
- **FastAPI**: Tune worker processes and connection pools
- **Docker**: Allocate sufficient CPU/memory resources
