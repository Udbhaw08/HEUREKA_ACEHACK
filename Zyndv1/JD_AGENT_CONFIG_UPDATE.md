# Job Description Agent - Configuration Update

## Summary

The Job Description/Extraction agent has been properly configured as a first-class microservice with configurable port and environment-based URL configuration.

---

## Changes Made

### 1. **Agent Client Configuration**

**File**: `backend/app/agent_client.py`

**Changes**:
- Added `os` import for environment variable access
- Made ALL agent endpoints configurable via environment variables
- Added `job_description` agent with dedicated endpoint

**Code**:
```python
self.endpoints = {
    "ats": os.getenv("ATS_SERVICE_URL", "http://localhost:8004") + "/run",
    "github": os.getenv("GITHUB_SERVICE_URL", "http://localhost:8005") + "/scrape",
    "leetcode": os.getenv("LEETCODE_SERVICE_URL", "http://localhost:8006") + "/scrape",
    "codeforces": os.getenv("CODEFORCES_SERVICE_URL", "http://localhost:8007") + "/scrape",
    "linkedin": os.getenv("LINKEDIN_SERVICE_URL", "http://localhost:8008") + "/parse",
    "skill": os.getenv("SKILL_SERVICE_URL", "http://localhost:8001") + "/run",
    "bias": os.getenv("BIAS_SERVICE_URL", "http://localhost:8002") + "/run",
    "matching": os.getenv("MATCHING_SERVICE_URL", "http://localhost:8003") + "/run",
    "passport": os.getenv("PASSPORT_SERVICE_URL", "http://localhost:8010") + "/issue",
    
    # Job Description / Extraction Agent
    "job_description": os.getenv("JOB_DESCRIPTION_SERVICE_URL", "http://localhost:8009") + "/extract",
}
```

---

### 2. **Job Router Update**

**File**: `backend/app/routers/job.py`

**Changes**:
- Added `AgentClient` import
- Updated skill extraction to use agent-based approach
- Added fallback to local extraction for backward compatibility

**Code**:
```python
# Use agent-based extraction (configurable port)
agent_client = AgentClient()
description = request.description or ""
print("Auto-extracting skills via job_description agent...")

jd_result = await agent_client._call_agent(
    "job_description",
    {
        "job_title": request.title,
        "job_description": description
    }
)

if jd_result.get("success"):
    extracted_data = jd_result.get("data", {})
else:
    # Fallback to local extraction if agent fails
    print(f"Agent extraction failed: {jd_result.get('error')}, falling back to local")
    extraction_agent = JobExtractionAgent()
    extracted_data = extraction_agent.extract(description, title=request.title)
```

---

### 3. **Environment Configuration**

**File**: `backend/.env.example`

**Changes**:
- Added `JOB_DESCRIPTION_SERVICE_URL=http://localhost:8009`
- Corrected port assignments for Codeforces (8007) and LinkedIn (8008)

**Updated Agent Services Section**:
```env
MATCHING_SERVICE_URL=http://localhost:8001
BIAS_SERVICE_URL=http://localhost:8002
SKILL_SERVICE_URL=http://localhost:8003
ATS_SERVICE_URL=http://localhost:8004
GITHUB_SERVICE_URL=http://localhost:8005
LEETCODE_SERVICE_URL=http://localhost:8006
CODEFORCES_SERVICE_URL=http://localhost:8007
LINKEDIN_SERVICE_URL=http://localhost:8008
JOB_DESCRIPTION_SERVICE_URL=http://localhost:8009
PASSPORT_SERVICE_URL=http://localhost:8010
```

---

### 4. **Documentation Updates**

**File**: `SETUP_GUIDE.md`

**Changes**:
- Added Job Description Agent to service port reference table
- Updated port 8009 assignment

---

## Architecture Benefits

### Before
- ❌ Job extraction hard-coded to local agent
- ❌ Not scalable independently
- ❌ Port not configurable
- ❌ Inconsistent with other agents

### After
- ✅ Job extraction as configurable microservice
- ✅ Can scale independently
- ✅ Port configurable via environment
- ✅ Consistent architecture across all agents
- ✅ Fallback to local extraction for resilience

---

## Port Assignments (Final)

| Service | Port | Environment Variable |
|---------|------|---------------------|
| Matching Agent | 8001 | MATCHING_SERVICE_URL |
| Bias Agent | 8002 | BIAS_SERVICE_URL |
| Skill Agent | 8003 | SKILL_SERVICE_URL |
| ATS Agent | 8004 | ATS_SERVICE_URL |
| GitHub Agent | 8005 | GITHUB_SERVICE_URL |
| LeetCode Agent | 8006 | LEETCODE_SERVICE_URL |
| Codeforces Agent | 8007 | CODEFORCES_SERVICE_URL |
| LinkedIn Agent | 8008 | LINKEDIN_SERVICE_URL |
| **Job Description Agent** | **8009** | **JOB_DESCRIPTION_SERVICE_URL** |
| Passport Agent | 8010 | PASSPORT_SERVICE_URL |

---

## Verification

### 1. Check Configuration

```bash
# Verify .env.example has JOB_DESCRIPTION_SERVICE_URL
cat backend/.env.example | grep JOB_DESCRIPTION

# Expected output:
# JOB_DESCRIPTION_SERVICE_URL=http://localhost:8009
```

### 2. Test Agent-Based Extraction

```bash
# Start backend
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8010

# Create a job (will attempt agent-based extraction)
curl -X POST http://localhost:8010/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "test_company",
    "title": "Senior Python Developer",
    "description": "Looking for Python expert with Django and AWS experience",
    "required_skills": [],
    "published": true
  }'

# Check logs for: "Auto-extracting skills via job_description agent..."
```

### 3. Test Fallback

```bash
# If job_description agent is not running, should see:
# "Agent extraction failed: ..., falling back to local"
# Job creation should still succeed
```

---

## Next Steps (Optional)

### Create Job Description Agent Service

If you want to run JD extraction as a separate service:

1. **Create service file**: `agents_services/job_description_service.py`
   ```python
   from flask import Flask, request, jsonify
   from app.agents.job_extraction import JobExtractionAgent
   
   app = Flask(__name__)
   extractor = JobExtractionAgent()
   
   @app.route('/extract', methods=['POST'])
   def extract():
       data = request.json
       result = extractor.extract(
           data['job_description'],
           title=data.get('job_title')
       )
       return jsonify(result)
   
   @app.route('/health', methods=['GET'])
   def health():
       return jsonify({"status": "healthy"})
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8009)
   ```

2. **Add to startup script**: `agents_services/start_all_complete.py`
   ```python
   services = [
       # ... existing services
       ("job_description_service.py", 8009),
   ]
   ```

---

## Rationale

This change aligns the Job Description extraction with the rest of the agent architecture:

1. **Consistency**: All agents now follow the same pattern
2. **Scalability**: JD extraction can be scaled independently
3. **Flexibility**: Port can be changed without code modifications
4. **Resilience**: Fallback ensures system continues working
5. **Deployment**: Easier to deploy agents on different machines/containers

---

**Update Version**: 1.0  
**Date**: 2026-02-03  
**Related**: Security Audit Fixes, Agent Architecture Standardization
