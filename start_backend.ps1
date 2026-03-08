# Start Backend API
$env:PYTHONPATH = "$PSScriptRoot\backend"
$VENV_PYTHON = "$PSScriptRoot\.venv\Scripts\python.exe"

Write-Host "Starting Backend API on port 8010..." -ForegroundColor Cyan

Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:PYTHONPATH='D:\ZyndHiring\Zyndv1\backend'; `$env:ZYND_WEBHOOK_HOST='0.0.0.0'; & '$VENV_PYTHON' -m uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload" -WindowStyle Normal

Write-Host "Backend API triggered." -ForegroundColor Green
