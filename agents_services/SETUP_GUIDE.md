# Complete Setup Guide - Agent Services

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Running the Services](#running-the-services)
4. [Verification](#verification)
5. [Common Issues](#common-issues)

---

## System Requirements

### Operating System
- ✅ **Windows**: 10 or 11
- ✅ **macOS**: 10.15 (Catalina) or later
- ✅ **Linux**: Ubuntu 20.04+, Debian 10+, or equivalent

### Software Requirements
- **Python**: 3.8 or higher (3.9+ recommended)
  - Check: `python --version` or `python3 --version`
- **pip**: Latest version
  - Check: `pip --version`
- **Git**: For cloning repositories (optional)
  - Check: `git --version`

### Hardware Requirements
- **RAM**: Minimum 4GB, 8GB+ recommended
- **Disk Space**: 2GB free space
- **Network**: Internet connection for API calls

### Port Availability
The following ports must be available:
- 8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008, 8009, 8011

---

## Installation Steps

### Step 1: Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH"
4. Verify installation:
   ```bash
   python --version
   ```

#### macOS
```bash
# Using Homebrew (recommended)
brew install python3

# Verify
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify
python3 --version
```

### Step 2: Navigate to Project Directory

```bash
# Windows
cd "C:\Users\<YourUsername>\Desktop\Agents-main (3) - Copy\Agents-main"

# macOS/Linux
cd ~/Desktop/Agents-main
```

### Step 3: Create Virtual Environment

**Why?** Isolates project dependencies from system Python.

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your command prompt.

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r agents_services/requirements.txt
```

**Expected output:**
```
Collecting fastapi
Collecting uvicorn
...
Successfully installed fastapi-0.x.x uvicorn-0.x.x ...
```

**If you get errors**, see [Common Issues](#common-issues) below.

### Step 5: Configure Environment Variables

Create a `.env` file in the `Agents-main` directory:

#### Windows (PowerShell)
```powershell
New-Item -Path .env -ItemType File
notepad .env
```

#### macOS/Linux
```bash
touch .env
nano .env
```

#### Add Required Variables

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here

# GitHub Configuration
GITHUB_TOKEN=ghp_your-token-here

# Database Configuration (if applicable)
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Other API Keys
LINKEDIN_API_KEY=your-key-here
LEETCODE_SESSION=your-session-here

# Optional: Python executable path
AGENT_PYTHON=python
```

**Where to get API keys:**
- OpenAI: https://platform.openai.com/api-keys
- GitHub: https://github.com/settings/tokens
- LinkedIn: https://www.linkedin.com/developers/

### Step 6: Verify Installation

```bash
# Test Python imports
python -c "import fastapi, uvicorn, pydantic; print('✅ Core dependencies OK')"

# Check environment file
python -c "from dotenv import load_dotenv; load_dotenv(); print('✅ .env file OK')"
```

---

## Running the Services

### Method 1: Batch File (Windows - Easiest)

1. Navigate to `agents_services` folder in File Explorer
2. Double-click `run_all_agents.bat`
3. Wait for all services to start

### Method 2: Python Script (All Platforms)

```bash
cd agents_services
python run_all_agents.py
```

### Method 3: Individual Services (For Testing)

```bash
cd agents_services

# Start one service at a time
python ats_service.py
# In a new terminal:
python github_service.py
# etc.
```

### Expected Output

```
================================================================================
🚀 Starting All Agent Services
================================================================================

Starting ATS Fraud Detection
  📄 Script: ats_service.py
  🔌 Port: 8004
  ⏳ Waiting for ATS Fraud Detection health check...
  ✓ ATS Fraud Detection is healthy!

[... continues for all services ...]

================================================================================
✅ All 10 services started successfully!
================================================================================

📡 Service Endpoints:
  • ATS Fraud Detection: http://localhost:8004
  • GitHub Analysis: http://localhost:8005
  [... etc ...]

Press Ctrl+C to stop all services
```

---

## Verification

### Test Individual Services

Open a browser or use `curl`:

```bash
# Test ATS Service
curl http://localhost:8004/health

# Expected response:
{"status":"healthy","service":"ats_fraud_detection","agent_loaded":true}

# Test all services
curl http://localhost:8001/health  # Matching
curl http://localhost:8002/health  # Bias
curl http://localhost:8003/health  # Skill
curl http://localhost:8004/health  # ATS
curl http://localhost:8005/health  # GitHub
curl http://localhost:8006/health  # LeetCode
curl http://localhost:8007/health  # LinkedIn
curl http://localhost:8008/health  # Passport
curl http://localhost:8009/health  # JD Assessment
curl http://localhost:8011/health  # Codeforces
```

### Check Logs

All services output logs in real-time. Look for:
- ✅ `Application startup complete`
- ✅ `Uvicorn running on http://0.0.0.0:XXXX`
- ❌ Any error messages or stack traces

---

## Common Issues

### Issue 1: `python: command not found`

**Solution:**
```bash
# Try python3 instead
python3 --version

# Or add Python to PATH (Windows)
# System Properties > Environment Variables > Path > Add Python directory
```

### Issue 2: `pip install` fails with permission error

**Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
# Activate and try again
```

### Issue 3: Port already in use

**Solution:**
```bash
# Windows
netstat -ano | findstr :8004
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8004 | xargs kill -9
```

### Issue 4: Virtual environment activation fails

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows CMD:**
```bash
venv\Scripts\activate.bat
```

### Issue 5: Import errors after installation

**Solution:**
```bash
# Ensure virtual environment is activated
# You should see (venv) in prompt

# Reinstall dependencies
pip install --upgrade pip
pip install -r agents_services/requirements.txt
```

### Issue 6: `.env` file not found

**Solution:**
```bash
# Ensure .env is in the correct location
# Should be in Agents-main/, NOT in agents_services/

# Check location
# Windows
dir .env
# macOS/Linux
ls -la .env
```

---

## Next Steps

1. ✅ All services running? → Test with sample requests
2. ✅ Need to stop? → Press `Ctrl+C`
3. ✅ Want to run on startup? → Create a system service
4. ✅ Deploy to production? → See deployment guide

---

## Quick Reference

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Update Dependencies
```bash
pip install --upgrade -r agents_services/requirements.txt
```

### Check Running Services
```bash
# Windows
netstat -ano | findstr :800

# macOS/Linux
lsof -i :8001-8011
```

### Stop All Services
```bash
# In the terminal running the script
Ctrl+C

# Or kill all Python processes (use with caution)
# Windows
taskkill /IM python.exe /F

# macOS/Linux
pkill -f python
```

---

**Need more help?** Check `RUN_AGENTS_README.md` for detailed troubleshooting.
