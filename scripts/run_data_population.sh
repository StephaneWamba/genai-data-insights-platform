#!/bin/bash

# ClickHouse Data Population Script Runner
# This script runs the data population script inside the ClickHouse container

echo "Starting ClickHouse data population..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Check if ClickHouse container is running
if ! docker-compose ps clickhouse | grep -q "Up"; then
    echo "Error: ClickHouse container is not running. Please start it first with: docker-compose up -d clickhouse"
    exit 1
fi

echo "Populating ClickHouse with realistic business data..."

# Copy the script to the container and run it
docker cp scripts/populate_clickhouse_data.py genaidatainsightsplatform-clickhouse-1:/tmp/
docker exec genaidatainsightsplatform-clickhouse-1 python3 /tmp/populate_clickhouse_data.py

if [ $? -eq 0 ]; then
    echo "Data population completed successfully!"
    echo ""
    echo "Data Summary:"
    echo "  - Sales records: ~4,500 (90 days × 50 records/day)"
    echo "  - Customer records: 500"
    echo "  - Inventory records: 125 (25 products × 5 stores each)"
    echo ""
    echo "You can now test the API endpoints with real data!"
else
    echo "Data population failed!"
    exit 1
fi 