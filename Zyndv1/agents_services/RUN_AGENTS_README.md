# Running All Agent Services

This directory contains scripts to easily start all 10 agent services simultaneously.

## � System Requirements

- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher (3.9+ recommended)
- **RAM**: Minimum 4GB (8GB+ recommended for all services)
- **Ports**: 8001-8009, 8011 must be available

## 🔧 Installation & Setup

### Step 1: Verify Python Installation

Check your Python version:
```bash
python --version
# or
python3 --version
```

**Expected output**: `Python 3.8.x` or higher

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

### Step 2: Create Virtual Environment (Recommended)

Navigate to the project root and create a virtual environment:

**Windows:**
```bash
cd "Agents-main"
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd Agents-main
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Install all required packages:
```bash
pip install -r agents_services/requirements.txt
```

**Common dependencies include:**
- FastAPI
- uvicorn
- pydantic
- python-dotenv
- And various AI/ML libraries

### Step 4: Configure Environment Variables

Create a `.env` file in the `Agents-main` directory (parent of `agents_services`):

```bash
# Example .env file
OPENAI_API_KEY=your_openai_key_here
GITHUB_TOKEN=your_github_token_here
LINKEDIN_API_KEY=your_linkedin_key_here
# Add other required API keys
```

**Required environment variables:**
- `OPENAI_API_KEY` - For AI-powered agents
- `GITHUB_TOKEN` - For GitHub service
- Database connection strings (if applicable)
- Other service-specific API keys

### Step 5: Verify Installation

Test that dependencies are installed:
```bash
python -c "import fastapi, uvicorn; print('Dependencies OK')"
```

## �🚀 Quick Start

**Now you're ready to run the services!**

### Option 1: Windows Batch File (Easiest)
Simply double-click on:
```
run_all_agents.bat
```

### Option 2: Python Script
Run from command line:
```bash
python run_all_agents.py
```

### Option 3: PowerShell
```powershell
cd Agents-main\agents_services
python run_all_agents.py
```

## 📋 Services Started

The script will start all 10 agent services:

| Service | Port | Endpoint |
|---------|------|----------|
| ATS Fraud Detection | 8004 | http://localhost:8004 |
| GitHub Analysis | 8005 | http://localhost:8005 |
| LeetCode Service | 8006 | http://localhost:8006 |
| Codeforces Service | 8011 | http://localhost:8011 |
| LinkedIn Service | 8007 | http://localhost:8007 |
| Skill Agent | 8003 | http://localhost:8003 |
| JD Assessment | 8009 | http://localhost:8009 |
| Bias Detection | 8002 | http://localhost:8002 |
| Matching Agent | 8001 | http://localhost:8001 |
| Passport Service | 8008 | http://localhost:8008 |

## ✨ Features

- **Colored Output**: Easy-to-read colored logs for each service
- **Health Checks**: Automatic verification that each service started correctly
- **Error Handling**: Clear error messages if a service fails to start
- **Graceful Shutdown**: Press Ctrl+C to stop all services cleanly
- **Real-time Logs**: See logs from all services in one terminal
- **Crash Detection**: Automatically detects if a service crashes

## 🔧 Requirements

- Python 3.8 or higher
- All dependencies installed (see `requirements.txt`)
- Environment variables configured (`.env` file in parent directory)

## 📝 Usage

1. Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure your `.env` file is configured in the parent directory

3. Run the script using one of the methods above

4. Wait for all services to start (you'll see health check confirmations)

5. Press **Ctrl+C** when you want to stop all services

## 🐛 Troubleshooting

### Common Error 1: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
Traceback (most recent call last):
  File "ats_service.py", line 6, in <module>
    from fastapi import FastAPI, HTTPException
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

### Common Error 2: Port Already in Use

**Error:**
```
OSError: [WinError 10048] Only one usage of each socket address is normally permitted
ERROR: Service ATS Fraud Detection died with code 1
```

**Solution:**
```bash
# Windows - Find and kill process using the port
netstat -ano | findstr :8004
taskkill /PID <process_id> /F

# macOS/Linux
lsof -ti:8004 | xargs kill -9
```

### Common Error 3: Python Version Mismatch

**Error:**
```
SyntaxError: invalid syntax
  processes: list[subprocess.Popen] = []
                  ^
```

**Solution:**
- You're using Python < 3.9
- Either upgrade Python or change the type hints:
```python
# Change from:
processes: list[subprocess.Popen] = []
# To:
from typing import List
processes: List[subprocess.Popen] = []
```

### Common Error 4: Missing Environment Variables

**Error:**
```
KeyError: 'OPENAI_API_KEY'
ERROR: ATS Agent initialization failed
```

**Solution:**
1. Create `.env` file in the parent directory
2. Add required keys:
```bash
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
```
3. Restart the services

### Common Error 5: Import Path Issues

**Error:**
```
ModuleNotFoundError: No module named 'skill_verification_agent'
  File "ats_service.py", line 32, in <module>
    from skill_verification_agent.agents.ats_guard import run_ats_guard
```

**Solution:**
```bash
# Ensure you're running from the correct directory
cd Agents-main/agents_services
python run_all_agents.py

# NOT from the parent directory
```

### Common Error 6: Health Check Timeout

**Error:**
```
⏳ Waiting for ATS Fraud Detection health check...
✗ ATS Fraud Detection health check failed: <urlopen error [WinError 10061]>
```

**Solution:**
1. Check service logs for the actual error
2. Common causes:
   - Missing dependencies
   - Database connection issues
   - API key problems
3. Increase timeout in script if needed (line 22):
```python
def wait_for_health(url: str, timeout_s: int = 60, ...):  # Increase from 30 to 60
```

### Platform-Specific Issues

#### Windows

**PowerShell Execution Policy Error:**
```
cannot be loaded because running scripts is disabled
```
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Colored Output Not Working:**
- Install Windows Terminal from Microsoft Store
- Or use Command Prompt instead of PowerShell

#### macOS

**SSL Certificate Errors:**
```bash
# Install certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

#### Linux

**Permission Denied:**
```bash
chmod +x run_all_agents.py
```

### Service-Specific Errors

#### ATS Service
- Requires PDF processing libraries
- May need additional system packages:
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils
```

#### GitHub Service
- Requires valid GitHub token
- Check rate limits: https://api.github.com/rate_limit

#### Database Services
- Ensure PostgreSQL/MySQL is running
- Verify connection strings in `.env`

### Getting More Help

If you encounter an error not listed here:

1. **Copy the full error message** including stack trace
2. **Note your environment:**
   - OS: Windows/macOS/Linux version
   - Python version: `python --version`
   - How you're running it: batch file, command line, etc.
3. **Check service logs** for more details
4. **Verify all setup steps** were completed

**Example bug report format:**
```
OS: Windows 11
Python: 3.10.5
Command: python run_all_agents.py

Error:
[Full stack trace here]

What I tried:
- Reinstalled dependencies
- Checked .env file
```

## 📊 Monitoring

The script provides real-time monitoring:
- Each service has a colored prefix in the logs
- Timestamps show when each log entry occurred
- Health checks confirm services are responding
- Automatic crash detection alerts you if a service dies

## 🛑 Stopping Services

To stop all services:
1. Press **Ctrl+C** in the terminal
2. The script will gracefully terminate all processes
3. Wait for the "All services stopped" message

## 🔄 Alternative Scripts

This directory also contains:
- `start_all.py` - Original startup script
- `start_all_complete.py` - Complete pipeline version

The new `run_all_agents.py` script provides enhanced features and better user experience.
