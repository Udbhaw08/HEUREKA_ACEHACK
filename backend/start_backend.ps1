# Start Backend Server Script
# This script starts the FastAPI backend server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Fair Hiring Backend Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\activate

# Check if .env file exists
if (!(Test-Path ".env")) {
    Write-Host "✗ .env file not found!" -ForegroundColor Red
    Write-Host "  Please create .env file with database configuration" -ForegroundColor Yellow
    exit 1
}

# Start the server
Write-Host "Starting backend server on http://localhost:8000" -ForegroundColor Green
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
