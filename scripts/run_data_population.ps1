# ClickHouse Data Population Script Runner (PowerShell)
# This script runs the data population script inside the ClickHouse container

Write-Host "Starting ClickHouse data population..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Check if ClickHouse container is running
$clickhouseStatus = docker-compose ps clickhouse
if ($clickhouseStatus -notmatch "Up") {
    Write-Host "Error: ClickHouse container is not running. Please start it first with: docker-compose up -d clickhouse" -ForegroundColor Red
    exit 1
}

Write-Host "Populating ClickHouse with realistic business data..." -ForegroundColor Yellow

# Copy the script to the container and run it
docker cp scripts/populate_clickhouse_data.py genaidatainsightsplatform-clickhouse-1:/tmp/
docker exec genaidatainsightsplatform-clickhouse-1 python3 /tmp/populate_clickhouse_data.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "Data population completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Data Summary:" -ForegroundColor Cyan
    Write-Host "  - Sales records: ~4,500 (90 days × 50 records/day)" -ForegroundColor White
    Write-Host "  - Customer records: 500" -ForegroundColor White
    Write-Host "  - Inventory records: 125 (25 products × 5 stores each)" -ForegroundColor White
    Write-Host ""
    Write-Host "You can now test the API endpoints with real data!" -ForegroundColor Green
}
else {
    Write-Host "Data population failed!" -ForegroundColor Red
    exit 1
} 