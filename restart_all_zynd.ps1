# Restart all Zynd agents with correct PYTHONPATH and 127.0.0.1 binding
$env:PYTHONPATH="."
$env:ZYND_WEBHOOK_HOST="127.0.0.1"
$env:ZYND_REGISTRY_URL="http://127.0.0.1:5100"

# Kill existing agents
Get-Process | Where-Object { $_.CommandLine -like "*zynd_integration.agents*" } | Stop-Process -Force -ErrorAction SilentlyContinue

echo "🚀 Starting Skill Agent..."
Start-Process .venv\Scripts\python.exe -ArgumentList "-m zynd_integration.agents.skill_agent" -NoNewWindow
echo "🚀 Starting Matching Agent..."
Start-Process .venv\Scripts\python.exe -ArgumentList "-m zynd_integration.agents.matching_agent" -NoNewWindow
echo "🚀 Starting ATS Agent..."
Start-Process .venv\Scripts\python.exe -ArgumentList "-m zynd_integration.agents.ats_agent" -NoNewWindow
echo "🚀 Starting GitHub Agent..."
Start-Process .venv\Scripts\python.exe -ArgumentList "-m zynd_integration.agents.github_agent" -NoNewWindow
echo "🚀 Starting LinkedIn Agent..."
Start-Process .venv\Scripts\python.exe -ArgumentList "-m zynd_integration.agents.linkedin_agent" -NoNewWindow
echo "🚀 Starting Passport Agent..."
Start-Process .venv\Scripts\python.exe -ArgumentList "-m zynd_integration.agents.passport_agent" -NoNewWindow

echo "✅ All agents started on 127.0.0.1 with PYTHONPATH=."
