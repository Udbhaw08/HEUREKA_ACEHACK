# ULTIMATE_DEMO_LAUNCHER.ps1
# Professional Multi-Agent Orchestration Launcher for Zynd Hackathon

$env:PYTHONPATH="backend;."
$env:USE_ZYND="1"
$env:ZYND_REGISTRY_URL="https://registry.zynd.ai"
$env:ZYND_WEBHOOK_HOST="127.0.0.1"

# Automatically detect venv or system python
$VENV_PY = "d:\ZyndHiring\Zyndv1\.venv\Scripts\python.exe"
if (Test-Path $VENV_PY) {
    $PYTHON_CMD = $VENV_PY
} else {
    $PYTHON_CMD = "python"
}

# Kill existing services
Write-Host "🛑 Cleaning up previous instances..." -ForegroundColor Red
$ports = 8012, 5100, 5101, 5102, 5103, 5104, 5105, 5106, 5107, 5109
foreach ($port in $ports) {
    if ($conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) {
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

# Run Reset Script
Write-Host "🧹 Resetting Database and Files..." -ForegroundColor Yellow
& $PYTHON_CMD reset_for_demo.py

Write-Host "`n🚀 Launching Agent Network..." -ForegroundColor Green

function Start-Agent {
    param ([string]$Name, [string]$Command, [string]$Color = "Cyan")
    Write-Host "  -> Starting $Name..." -ForegroundColor $Color
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { `$Host.UI.RawUI.WindowTitle = '$Name'; `$env:PYTHONPATH='backend;.'; `$env:USE_ZYND='1'; & '$PYTHON_CMD' -m $Command }"
}

# 1. CORE SYSTEM
Start-Agent "CORE BACKEND (Port 8012)" "uvicorn app.main:app --host 127.0.0.1 --port 8012 --log-level info" "White"
Start-Sleep -s 3

# 2. VERIFICATION CLUSTER
Start-Agent "VERIFIER: Skill Agent (5103)" "zynd_integration.agents.skill_agent"
Start-Agent "VERIFIER: Passport Agent (5105)" "zynd_integration.agents.passport_agent"
Start-Agent "VERIFIER: Matching Agent (5101)" "zynd_integration.agents.matching_agent"

# 3. AUDIT & TEST CLUSTER
Start-Agent "AUDITOR: Bias Detection (5102)" "zynd_integration.agents.bias_agent"
Start-Agent "AUDITOR: ATS Trust Guard (5104)" "zynd_integration.agents.ats_agent"
Start-Agent "TESTER: AI Interview Agent (5109)" "zynd_integration.agents.skill_test_agent"

# 4. SOURCE CLUSTER
Start-Agent "SOURCE: GitHub Parser (5106)" "zynd_integration.agents.github_agent"
Start-Agent "SOURCE: LinkedIn Parser (5107)" "zynd_integration.agents.linkedin_agent"
