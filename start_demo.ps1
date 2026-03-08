# start_demo.ps1 - Demo Mode Startup (Visible Windows)
# Launches each agent in its own terminal window so logs are visible.

$env:PYTHONPATH="backend;."
$env:ZYND_REGISTRY_URL="https://registry.zynd.ai"
$env:ZYND_WEBHOOK_HOST="0.0.0.0"
$env:USE_ZYND="1"

$ports = 5100, 5101, 5102, 5103, 5104, 5105, 5106, 5107
foreach ($port in $ports) {
    Write-Host "Checking port $port..."
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conns) {
        foreach ($conn in $conns) {
            $proc_id = $conn.OwningProcess
            if ($proc_id -gt 0) {
                Write-Host "Killing process $proc_id on port $port"
                Stop-Process -Id $proc_id -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

Start-Sleep -s 3

# Function to start a visible agent window with auto-hold on error
function Start-VisibleAgent {
    param (
        [string]$Name,
        [string]$Command,
        [string]$Port
    )
    Write-Host "Starting $Name ($Port)..."
    # We launch a new PowerShell process that activates venv (if needed) and runs the module
    # We use -NoExit so the window stays open if it crashes, allowing debugging
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { `$env:PYTHONPATH='backend;.'; `$env:USE_ZYND='1'; `$env:ZYND_WEBHOOK_HOST='0.0.0.0'; `$Host.UI.RawUI.WindowTitle = '$Name ($Port)'; python -m $Command }"
    Start-Sleep -s 2
}

# 1. Backend
Start-VisibleAgent -Name "BACKEND API" -Command "uvicorn app.main:app --host 0.0.0.0 --port 8012 --log-level info" -Port "8012"

# 2. Matching Agent
Start-VisibleAgent -Name "MATCHING AGENT" -Command "zynd_integration.agents.matching_agent" -Port "5101"

# 3. Bias Agent
Start-VisibleAgent -Name "BIAS AGENT" -Command "zynd_integration.agents.bias_agent" -Port "5102"

# 4. Skill Agent
Start-VisibleAgent -Name "SKILL AGENT" -Command "zynd_integration.agents.skill_agent" -Port "5103"

# 5. ATS Agent
Start-VisibleAgent -Name "ATS AGENT" -Command "zynd_integration.agents.ats_agent" -Port "5104"

# 6. Passport Agent
Start-VisibleAgent -Name "PASSPORT AGENT" -Command "zynd_integration.agents.passport_agent" -Port "5105"

# 7. GitHub Agent
Start-VisibleAgent -Name "GITHUB AGENT" -Command "zynd_integration.agents.github_agent" -Port "5106"

# 8. LinkedIn Agent
Start-VisibleAgent -Name "LINKEDIN AGENT" -Command "zynd_integration.agents.linkedin_agent" -Port "5107"

Write-Host "
================================================================
 DEMO MODE STARTED
================================================================
All agents are running in separate windows.
Arrange them on your screen to show activity during the demo.
Backend API: http://localhost:8012
Frontend:    http://localhost:5173 (run 'npm run dev' separately)
================================================================
"
