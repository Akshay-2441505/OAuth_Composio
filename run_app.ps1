# OAuth Compass — Startup Helper
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Starting OAuth Compass Development Environment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Start Backend in new process
Write-Host "[1/2] Starting FastAPI backend on http://localhost:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000"

# Start Frontend in new process
Write-Host "[2/2] Starting Vite React frontend on http://localhost:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "Both servers launched!" -ForegroundColor Cyan
Write-Host "Open your browser at: http://localhost:5173" -ForegroundColor Yellow

