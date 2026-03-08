# Fair Hiring Platform - Product Requirements Document (PRD)

**Version:** 1.0  
**Last Updated:** February 9, 2026  
**Project Status:** Active Development  
**Handoff Purpose:** Complete project documentation for ChatGPT debugging, analysis, and development

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [System Architecture](#system-architecture)
4. [Core Components](#core-components)
5. [Technical Stack](#technical-stack)
6. [Database Schema](#database-schema)
7. [API Documentation](#api-documentation)
8. [Agent Services](#agent-services)
9. [Pipeline Workflow](#pipeline-workflow)
10. [Setup & Installation](#setup--installation)
11. [Development Guide](#development-guide)
12. [Debugging Guide](#debugging-guide)
13. [Known Issues](#known-issues)
14. [Future Roadmap](#future-roadmap)
15. [Appendix](#appendix)

---

## 1. Executive Summary

### What is This Project?

The **Fair Hiring Platform** is an end-to-end AI-powered recruitment system designed to eliminate bias and fraud in the hiring process. It uses multiple AI agents to verify candidate skills, detect resume fraud, identify hiring bias, and generate cryptographically signed skill passports.

### Key Features

- ✅ **Multi-Source Skill Verification** - Validates skills from GitHub, LeetCode, Codeforces, and LinkedIn
- ✅ **Fraud Detection** - ATS agent screens for resume manipulation and hidden text
- ✅ **Bias Detection** - Identifies discriminatory patterns in hiring decisions
- ✅ **Skill Passport** - Cryptographically signed, portable credentials (Ed25519)
- ✅ **Intelligent Matching** - Semantic matching between candidates and job requirements
- ✅ **Human-in-Loop** - Review queue for flagged applications
- ✅ **Real-time Dashboards** - Live metrics for candidates and companies

### Current Status

| Component | Status | Completion |
|-----------|--------|------------|
| Backend API | ✅ Working | 95% |
| Frontend | ✅ Working | 90% |
| Agent Services | ⚠️ Partial | 70% |
| Database | ✅ Working | 100% |
| Pipeline | ⚠️ Needs Integration | 60% |
| Documentation | ✅ Complete | 100% |

---

## 2. Project Overview

### Problem Statement

Traditional hiring processes suffer from:
1. **Resume Fraud** - Fake skills, inflated experience, hidden keywords
2. **Bias** - Unconscious discrimination based on gender, college, background
3. **Inefficiency** - Manual verification of skills is time-consuming
4. **Lack of Trust** - No verifiable proof of candidate skills

### Solution

A multi-agent system that:
1. **Automatically verifies** skills across multiple platforms
2. **Detects and prevents** resume fraud using AI
3. **Identifies and flags** biased hiring patterns
4. **Generates portable** cryptographically signed skill credentials
5. **Matches candidates** to jobs using semantic analysis

### Target Users

1. **Candidates**
   - Create profile with anonymous ID
   - Apply to jobs
   - View skill passport
   - Track application status

2. **Companies**
   - Post job openings
   - Review candidate pipelines
   - Run matching algorithms
   - Access fairness reports

3. **System Administrators**
   - Review flagged applications
   - Monitor agent performance
   - Manage bias detection rules

---

## 3. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                         │
│                   Port: 5173 (Vite)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Candidate   │  │   Company    │  │    Admin     │      │
│  │  Dashboard   │  │  Dashboard   │  │   Review     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API
┌──────────────────────────▼──────────────────────────────────┐
│                   BACKEND (FastAPI)                          │
│                    Port: 8000/8010                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Pipeline Orchestrator                         │   │
│  │  (Coordinates 10-stage verification workflow)         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Auth    │  │   Jobs   │  │  Apply   │  │ Passport │   │
│  │  Router  │  │  Router  │  │  Router  │  │  Router  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │ SQL Queries
┌──────────────────────────▼──────────────────────────────────┐
│                   DATABASE (PostgreSQL)                      │
│                        Port: 5432                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  users   │  │candidates│  │   jobs   │  │  apps    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  creds   │  │  reviews │  │blacklist │  │ passports│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP Calls
┌──────────────────────────▼──────────────────────────────────┐
│                  AGENT SERVICES (10 Microservices)          │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   ATS    │  │  GitHub  │  │ LeetCode │  │Codeforce │   │
│  │  :8004   │  │  :8005   │  │  :8006   │  │  :8011   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ LinkedIn │  │  Skill   │  │ Cond.Test│  │   Bias   │   │
│  │  :8007   │  │  :8003   │  │  :8009   │  │  :8002   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐                                │
│  │ Matching │  │ Passport │                                │
│  │  :8001   │  │  :8008   │                                │
│  └──────────┘  └──────────┘                                │
└───────────────────────────────────────────────────────────────┘
```

### Component Communication

1. **Frontend → Backend**: REST API calls (JSON)
2. **Backend → Database**: Async SQLAlchemy (asyncpg)
3. **Backend → Agents**: HTTP POST requests (JSON)
4. **Agents → External APIs**: GitHub API, LeetCode scraping, etc.

### Data Flow

```
Candidate Applies
    ↓
Backend creates Application record
    ↓
Pipeline Orchestrator triggered
    ↓
Stage 1: ATS Agent (fraud detection)
    ├─ PASS → Continue
    ├─ NEEDS_REVIEW → Queue for human review
    └─ BLACKLIST → Reject immediately
    ↓
Stage 2-5: Scraper Agents (parallel)
    ├─ GitHub Agent → Repositories, commits, languages
    ├─ LeetCode Agent → Problems solved, contest rating
    ├─ Codeforces Agent → Rating, submissions
    └─ LinkedIn Agent → Experience, education
    ↓
Stage 6: Skill Agent (aggregation)
    ├─ Combine evidence from all sources
    ├─ Calculate confidence scores
    └─ Determine if test required
    ↓
Stage 7: Conditional Test (if needed)
    ├─ Generate skill-specific test
    ├─ PAUSE pipeline
    └─ Resume after test completion
    ↓
Stage 8: Bias Detection
    ├─ Analyze hiring patterns
    ├─ Check for discrimination
    └─ Flag systemic issues
    ↓
Stage 9: Matching Agent
    ├─ Compare skills to job requirements
    ├─ Calculate match score
    └─ Identify skill gaps
    ↓
Stage 10: Passport Agent
    ├─ Generate credential JSON
    ├─ Sign with Ed25519 private key
    └─ Store in database
    ↓
Update Application status
    ↓
Notify Candidate
```

---

## 4. Core Components

### 4.1 Frontend (React + Vite)

**Location:** `fair-hiring-frontend/`

**Key Features:**
- Candidate signup/login with anonymous ID
- Job browsing and application
- Skill passport visualization
- Company dashboard with candidate pipelines
- Job creation and management
- Real-time status updates

**Tech Stack:**
- React 18
- Vite (build tool)
- TailwindCSS (styling)
- React Router (navigation)
- Axios (API calls)

**Key Files:**
```
fair-hiring-frontend/
├── src/
│   ├── components/
│   │   ├── CandidateDashboard.jsx
│   │   ├── CompanyDashboard.jsx
│   │   ├── CompanyHiringFlow.jsx
│   │   ├── CompanyRolePipeline.jsx
│   │   ├── SkillPassport.jsx
│   │   └── JobPostingForm.jsx
│   ├── api/
│   │   └── client.js
│   ├── App.jsx
│   └── main.jsx
├── package.json
└── vite.config.js
```

### 4.2 Backend (FastAPI)

**Location:** `backend/`

**Key Features:**
- RESTful API with async support
- JWT-like authentication
- Pipeline orchestration
- Database ORM (SQLAlchemy)
- CORS configuration
- File upload handling

**Tech Stack:**
- FastAPI (web framework)
- SQLAlchemy (async ORM)
- asyncpg (PostgreSQL driver)
- Pydantic (validation)
- Uvicorn (ASGI server)

**Key Files:**
```
backend/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── passport.py          # Ed25519 signing
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── candidate.py     # Candidate endpoints
│   │   ├── company.py       # Company endpoints
│   │   ├── job.py           # Job endpoints
│   │   ├── application.py   # Application endpoints
│   │   └── pipeline.py      # Pipeline endpoints
│   └── services/
│       ├── pipeline_service.py  # Orchestrator
│       └── agent_client.py      # Agent HTTP client
├── uploads/                 # Resume uploads
├── requirements.txt
└── .env
```

### 4.3 Agent Services

**Location:** `agents_services/`

**Purpose:** Independent microservices for specific verification tasks

**Services:**

| Service | Port | Status | Purpose |
|---------|------|--------|---------|
| ATS Service | 8004 | ✅ Working | Resume fraud detection |
| GitHub Service | 8005 | ✅ Working | Repository analysis |
| LeetCode Service | 8006 | ✅ Working | Coding problem verification |
| Codeforces Service | 8011 | ✅ Working | Competitive programming |
| LinkedIn Service | 8007 | ✅ Working | Professional history |
| Skill Service | 8003 | ⚠️ Mock | Skill aggregation |
| Conditional Test | 8009 | ✅ Working | Test generation |
| Bias Service | 8002 | ⚠️ Mock | Bias detection |
| Matching Service | 8001 | ⚠️ Mock | Job matching |
| Passport Service | 8008 | ✅ Working | Credential signing |

**Common Structure:**
```python
# Example: ats_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ATS Service")

class ATSRequest(BaseModel):
    resume_text: str
    resume_path: str = None

class ATSResponse(BaseModel):
    action: str  # OK | NEEDS_REVIEW | BLACKLIST
    fraud_detected: bool
    manipulation_signals: dict

@app.post("/analyze")
async def analyze_resume(request: ATSRequest):
    # Fraud detection logic
    return ATSResponse(...)

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### 4.4 Agent Core Logic

**Location:** `agents_files/Clean_Hiring_System/`

**Purpose:** Core AI agent implementations

**Key Agents:**
- `skill_verification_agent/` - Skill extraction and verification
- `bias_detection_agent/` - Bias pattern detection
- `matching_agent/` - Semantic job matching
- `ats_agent/` - Fraud detection (ATS Guard)
- `passport_agent/` - Credential generation

---

## 5. Technical Stack

### Languages & Frameworks

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Frontend | React | 18.x | UI framework |
| Frontend Build | Vite | 4.x | Build tool |
| Backend | FastAPI | 0.100+ | API framework |
| Backend Runtime | Python | 3.10+ | Programming language |
| Database | PostgreSQL | 14+ | Data storage |
| Agent Services | FastAPI/Flask | - | Microservices |
| Styling | TailwindCSS | 3.x | CSS framework |

### Key Libraries

**Backend:**
```
fastapi==0.100.0
uvicorn==0.23.0
sqlalchemy==2.0.0
asyncpg==0.28.0
pydantic==2.0.0
python-dotenv==1.0.0
httpx==0.24.0
cryptography==41.0.0
bcrypt==4.0.0
```

**Frontend:**
```
react==18.2.0
react-router-dom==6.14.0
axios==1.4.0
tailwindcss==3.3.0
```

**Agents:**
```
langchain==0.0.200
ollama==0.1.0
beautifulsoup4==4.12.0
selenium==4.10.0
requests==2.31.0
```

### External APIs & Services

1. **GitHub API** - Repository analysis
   - Requires: `GITHUB_TOKEN`
   - Rate limit: 5000 requests/hour

2. **LeetCode** - Web scraping (no official API)
   - Requires: Session cookies
   - Rate limit: Aggressive throttling

3. **Codeforces API** - Public API
   - No authentication required
   - Rate limit: 1 request/2 seconds

4. **LinkedIn** - PDF parsing (no API access)
   - Requires: Manual PDF upload

5. **OpenAI/Ollama** - LLM for analysis
   - Requires: `OPENAI_API_KEY` or local Ollama

---

## 6. Database Schema

### Entity Relationship Diagram

```
┌─────────────┐         ┌─────────────┐
│    users    │         │  companies  │
│─────────────│         │─────────────│
│ id (PK)     │         │ id (PK)     │
│ email       │         │ name        │
│ password    │         │ email       │
│ role        │         │ user_id(FK) │
│ created_at  │         └─────────────┘
└──────┬──────┘                │
       │                       │
       │ 1:1                   │ 1:N
       │                       │
┌──────▼──────┐         ┌──────▼──────┐
│ candidates  │         │    jobs     │
│─────────────│         │─────────────│
│ id (PK)     │         │ id (PK)     │
│ user_id(FK) │         │ company_id  │
│ anon_id     │         │ title       │
│ name        │         │ description │
│ github_url  │         │ requirements│
│ leetcode_url│         │ status      │
│ college     │         │ created_at  │
│ gender      │         └──────┬──────┘
└──────┬──────┘                │
       │                       │
       │ N:M                   │
       │                       │
       └───────┬───────────────┘
               │
        ┌──────▼──────────┐
        │  applications   │
        │─────────────────│
        │ id (PK)         │
        │ candidate_id(FK)│
        │ job_id (FK)     │
        │ status          │
        │ match_score     │
        │ test_required   │
        │ feedback_json   │
        │ applied_at      │
        └──────┬──────────┘
               │
               │ 1:1
               │
        ┌──────▼──────────┐
        │  credentials    │
        │─────────────────│
        │ id (PK)         │
        │ candidate_id(FK)│
        │ application_id  │
        │ credential_json │
        │ hash_sha256     │
        │ signature_b64   │
        │ issued_at       │
        └─────────────────┘
```

### Table Definitions

#### users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'candidate' | 'company' | 'admin'
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### candidates
```sql
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    anon_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255),
    github_url VARCHAR(500),
    leetcode_url VARCHAR(500),
    codeforces_url VARCHAR(500),
    linkedin_url VARCHAR(500),
    college VARCHAR(255),
    gender VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### companies
```sql
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### jobs
```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    requirements JSONB,  -- {required_skills: [], preferred_skills: []}
    status VARCHAR(20) DEFAULT 'published',
    fairness_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### applications
```sql
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    status VARCHAR(50) DEFAULT 'pending',
    match_score FLOAT,
    test_required BOOLEAN DEFAULT FALSE,
    feedback_json JSONB,
    applied_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### credentials
```sql
CREATE TABLE credentials (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    application_id INTEGER REFERENCES applications(id),
    credential_json JSONB NOT NULL,
    hash_sha256 VARCHAR(64) NOT NULL,
    signature_b64 TEXT NOT NULL,
    issued_at TIMESTAMP DEFAULT NOW()
);
```

#### review_cases
```sql
CREATE TABLE review_cases (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    job_id INTEGER REFERENCES jobs(id),
    candidate_id INTEGER REFERENCES candidates(id),
    triggered_by VARCHAR(50),  -- 'ATS' | 'BIAS_DETECTION'
    severity VARCHAR(20),
    reason TEXT,
    evidence JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    reviewed_by INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### blacklist
```sql
CREATE TABLE blacklist (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    reason TEXT,
    evidence JSONB,
    blacklisted_at TIMESTAMP DEFAULT NOW()
);
```

---

## 7. API Documentation

### Base URL
- **Development:** `http://localhost:8000` or `http://localhost:8010`
- **Production:** TBD

### Authentication

All authenticated endpoints require a token in the header:
```
Authorization: Bearer <token>
```

### Endpoints

#### 7.1 Authentication

**POST /api/auth/signup/candidate**
```json
Request:
{
  "email": "candidate@example.com",
  "password": "securepassword",
  "name": "John Doe",
  "github_url": "https://github.com/johndoe",
  "leetcode_url": "https://leetcode.com/johndoe"
}

Response:
{
  "anon_id": "anon_abc123",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "Candidate registered successfully"
}
```

**POST /api/auth/signup/company**
```json
Request:
{
  "email": "company@example.com",
  "password": "securepassword",
  "company_name": "TechCorp Inc."
}

Response:
{
  "company_id": 1,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "Company registered successfully"
}
```

**POST /api/auth/login**
```json
Request:
{
  "email": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "role": "candidate",
  "user_id": 1
}
```

#### 7.2 Jobs

**GET /api/jobs**
```json
Response:
[
  {
    "id": 1,
    "title": "Senior Backend Engineer",
    "company_name": "TechCorp",
    "description": "Looking for Python FastAPI expert...",
    "requirements": {
      "required_skills": ["Python", "FastAPI", "PostgreSQL"],
      "preferred_skills": ["Docker", "Kubernetes"]
    },
    "created_at": "2026-02-01T10:00:00Z"
  }
]
```

**POST /api/jobs** (Company only)
```json
Request:
{
  "title": "Senior Backend Engineer",
  "description": "Looking for Python FastAPI expert...",
  "requirements": {
    "required_skills": ["Python", "FastAPI"],
    "preferred_skills": ["Docker"]
  }
}

Response:
{
  "job_id": 1,
  "message": "Job created successfully"
}
```

#### 7.3 Applications

**POST /api/applications**
```json
Request:
{
  "job_id": 1,
  "anon_id": "anon_abc123",
  "resume_file": "<multipart/form-data>"
}

Response:
{
  "application_id": 42,
  "status": "pending",
  "message": "Application submitted. Pipeline running..."
}
```

**GET /api/applications/{id}**
```json
Response:
{
  "id": 42,
  "job_title": "Senior Backend Engineer",
  "status": "matched",
  "match_score": 85.5,
  "feedback": {
    "matched_skills": ["Python", "FastAPI"],
    "missing_skills": ["Kubernetes"]
  },
  "applied_at": "2026-02-09T10:00:00Z"
}
```

#### 7.4 Pipeline

**POST /api/pipeline/run**
```json
Request:
{
  "application_id": 42
}

Response:
{
  "status": "running",
  "stages_completed": ["ATS", "GITHUB"],
  "current_stage": "LEETCODE"
}
```

**GET /api/pipeline/status/{application_id}**
```json
Response:
{
  "application_id": 42,
  "pipeline_status": "completed",
  "stages_completed": ["ATS", "GITHUB", "LEETCODE", "SKILL", "BIAS", "MATCHING", "PASSPORT"],
  "credential_id": 15
}
```

#### 7.5 Passport

**GET /api/passport/{candidate_id}**
```json
Response:
{
  "candidate_id": 1,
  "anon_id": "anon_abc123",
  "credentials": [
    {
      "id": 15,
      "application_id": 42,
      "verified_skills": ["Python", "FastAPI", "PostgreSQL"],
      "confidence_scores": {
        "Python": 0.95,
        "FastAPI": 0.88,
        "PostgreSQL": 0.75
      },
      "evidence": {
        "github": {...},
        "leetcode": {...}
      },
      "signature": "MEUCIQDx...",
      "issued_at": "2026-02-09T11:00:00Z"
    }
  ]
}
```

---

## 8. Agent Services

### 8.1 ATS Service (Port 8004)

**Purpose:** Detect resume fraud and manipulation

**Endpoint:** `POST /analyze`

**Request:**
```json
{
  "resume_text": "Full resume text...",
  "resume_path": "/uploads/resume.pdf"
}
```

**Response:**
```json
{
  "action": "OK",  // OK | NEEDS_REVIEW | BLACKLIST
  "fraud_detected": false,
  "manipulation_detected": false,
  "severity": "none",
  "manipulation_signals": {
    "white_text_count": 0,
    "prompt_injection": false,
    "bot_generated": false,
    "trust_score": 95
  }
}
```

**Detection Methods:**
- White text detection (hidden keywords)
- Prompt injection attempts
- Bot-generated content
- PDF layer analysis
- Image text extraction
- Timeline consistency checks

### 8.2 GitHub Service (Port 8005)

**Purpose:** Analyze GitHub repositories

**Endpoint:** `POST /scrape`

**Request:**
```json
{
  "username": "Udbhaw08"
}
```

**Response:**
```json
{
  "username": "Udbhaw08",
  "repositories": [
    {
      "name": "fair-hiring-platform",
      "languages": ["Python", "JavaScript"],
      "stars": 15,
      "commits": 127
    }
  ],
  "total_commits": 450,
  "top_languages": ["Python", "JavaScript", "Go"],
  "account_age_days": 1825
}
```

### 8.3 LeetCode Service (Port 8006)

**Purpose:** Verify algorithmic problem-solving skills

**Endpoint:** `POST /scrape`

**Request:**
```json
{
  "username": "johndoe"
}
```

**Response:**
```json
{
  "username": "johndoe",
  "problems_solved": 250,
  "difficulty_breakdown": {
    "easy": 100,
    "medium": 120,
    "hard": 30
  },
  "contest_rating": 1850,
  "badges": ["50 Days Badge", "Annual Badge 2025"]
}
```

### 8.4 Skill Service (Port 8003)

**Purpose:** Aggregate evidence and calculate confidence

**Endpoint:** `POST /run`

**Request:**
```json
{
  "application_id": 42,
  "resume_text": "...",
  "github_url": "https://github.com/johndoe",
  "leetcode_url": "https://leetcode.com/johndoe",
  "anon_id": "anon_abc123"
}
```

**Response:**
```json
{
  "output": {
    "skills": ["Python", "FastAPI", "React", "PostgreSQL"],
    "confidence": 0.85,
    "signal_strength": "strong",
    "test_required": false
  },
  "explanation": "Strong evidence from GitHub (50+ commits) and LeetCode (250 problems)",
  "flags": []
}
```

### 8.5 Matching Service (Port 8001)

**Purpose:** Match candidates to job requirements

**Endpoint:** `POST /run`

**Request:**
```json
{
  "credential": {
    "skills": ["Python", "FastAPI"],
    "confidence": 0.85
  },
  "job_description": {
    "title": "Backend Engineer",
    "description": "Looking for Python FastAPI expert...",
    "required_skills": ["Python", "FastAPI", "PostgreSQL"]
  }
}
```

**Response:**
```json
{
  "match_score": 85.5,
  "matched_skills": ["Python", "FastAPI"],
  "missing_skills": ["PostgreSQL"],
  "recommendation": "Strong match. Consider for interview.",
  "breakdown": {
    "core_skills": 90,
    "frameworks": 85,
    "experience": 80
  }
}
```

---

## 9. Pipeline Workflow

### Complete 10-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION SUBMITTED                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  STAGE 1:   │
                    │  ATS AGENT  │
                    │  (Fraud)    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         BLACKLIST    NEEDS_REVIEW     OK
              │            │            │
         [REJECT]    [QUEUE HUMAN]     │
                           │            │
                    ┌──────▼──────┐    │
                    │   HUMAN     │    │
                    │   REVIEW    │    │
                    └──────┬──────┘    │
                           │            │
                      APPROVED          │
                           │            │
                           └────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  STAGE 2-5: SCRAPERS      │
                    │  (Parallel Execution)     │
                    │  ┌──────┐  ┌──────┐      │
                    │  │GitHub│  │LCode │      │
                    │  └──────┘  └──────┘      │
                    │  ┌──────┐  ┌──────┐      │
                    │  │CForce│  │LnkdIn│      │
                    │  └──────┘  └──────┘      │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  STAGE 6: SKILL AGENT     │
                    │  (Evidence Aggregation)   │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  Decision: Test Required? │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │                           │
                   YES                         NO
                    │                           │
        ┌───────────▼───────────┐              │
        │  STAGE 7: COND. TEST  │              │
        │  (Generate Test)      │              │
        └───────────┬───────────┘              │
                    │                           │
              [PAUSE PIPELINE]                  │
                    │                           │
           ┌────────▼────────┐                 │
           │ Candidate Takes │                 │
           │      Test       │                 │
           └────────┬────────┘                 │
                    │                           │
              [RESUME PIPELINE]                 │
                    │                           │
                    └───────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  STAGE 8: BIAS DETECTION  │
                    │  (Fairness Check)         │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  STAGE 9: MATCHING AGENT  │
                    │  (Job Fit Score)          │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  STAGE 10: PASSPORT AGENT │
                    │  (Sign Credential)        │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  UPDATE APPLICATION       │
                    │  - Status: matched/rejected│
                    │  - Match Score            │
                    │  - Credential ID          │
                    └───────────────────────────┘
```

### State Management

The pipeline maintains state in `credential_json`:

```json
{
  "application_id": 42,
  "pipeline_status": "completed",
  "stages_completed": ["ATS", "GITHUB", "LEETCODE", "SKILL", "BIAS", "MATCHING", "PASSPORT"],
  "evidence": {
    "ats": {
      "action": "OK",
      "trust_score": 95
    },
    "github": {
      "repositories": [...],
      "total_commits": 450
    },
    "leetcode": {
      "problems_solved": 250
    },
    "skills": {
      "verified_skills": ["Python", "FastAPI"],
      "confidence": 0.85
    },
    "bias": {
      "bias_detected": false
    },
    "matching": {
      "match_score": 85.5
    }
  },
  "verified_skills": ["Python", "FastAPI", "React"],
  "confidence": 0.85,
  "match_score": 85.5,
  "credential_id": 15
}
```

---

## 10. Setup & Installation

### Prerequisites

- **Operating System:** Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python:** 3.10 or higher
- **Node.js:** 18 or higher
- **PostgreSQL:** 14 or higher
- **Git:** Latest version

### Step-by-Step Setup

#### 1. Clone Repository

```bash
git clone <repository-url>
cd Agents-main
```

#### 2. Database Setup

```bash
# Start PostgreSQL
# Windows: Start PostgreSQL service
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database
createdb fair_hiring

# Or using psql
psql -U postgres
CREATE DATABASE fair_hiring;
\q
```

#### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python create_database.py
python create_tables.py

# Start backend
uvicorn app.main:app --reload --port 8000
```

#### 4. Agent Services Setup

```bash
cd agents_services

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start all services
python run_all_agents.py

# Or use batch file (Windows)
run_all_agents.bat
```

#### 5. Frontend Setup

```bash
cd fair-hiring-frontend

# Install dependencies
npm install

# Configure environment
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# Start development server
npm run dev
```

### Environment Variables

#### Backend `.env`

```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/fair_hiring

# Agent Services
ATS_SERVICE_URL=http://localhost:8004
GITHUB_SERVICE_URL=http://localhost:8005
LEETCODE_SERVICE_URL=http://localhost:8006
CODEFORCES_SERVICE_URL=http://localhost:8011
LINKEDIN_SERVICE_URL=http://localhost:8007
SKILL_SERVICE_URL=http://localhost:8003
CONDITIONAL_TEST_SERVICE_URL=http://localhost:8009
BIAS_SERVICE_URL=http://localhost:8002
MATCHING_SERVICE_URL=http://localhost:8001
PASSPORT_SERVICE_URL=http://localhost:8008

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ED25519_PRIVATE_KEY=base64-encoded-private-key
ED25519_PUBLIC_KEY=base64-encoded-public-key

# CORS
FRONTEND_URL=http://localhost:5173

# External APIs
GITHUB_TOKEN=ghp_your_github_token
OPENAI_API_KEY=sk-your-openai-key

# Agent Settings
AGENT_TIMEOUT=60
DEBUG=true
```

#### Frontend `.env`

```bash
VITE_API_BASE_URL=http://localhost:8000
```

### Verification

```bash
# Check backend
curl http://localhost:8000/health

# Check agent services
curl http://localhost:8004/health
curl http://localhost:8005/health
# ... etc for all services

# Check frontend
# Open browser: http://localhost:5173
```

---

## 11. Development Guide

### Adding a New Agent Service

1. **Create Service File**

```python
# agents_services/new_agent_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="New Agent Service")

class NewAgentRequest(BaseModel):
    input_data: str

class NewAgentResponse(BaseModel):
    output_data: dict

@app.post("/run")
async def run_agent(request: NewAgentRequest):
    # Agent logic here
    return NewAgentResponse(output_data={})

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
```

2. **Update `run_all_agents.py`**

```python
services = [
    # ... existing services ...
    ("new_agent_service.py", 8012, "http://localhost:8012/health", "New Agent", Colors.OKGREEN),
]
```

3. **Add to Backend**

```python
# backend/app/config.py
NEW_AGENT_SERVICE_URL = os.getenv("NEW_AGENT_SERVICE_URL", "http://localhost:8012")

# backend/app/services/pipeline_service.py
async def run_new_agent(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{config.NEW_AGENT_SERVICE_URL}/run", json=data)
        return response.json()
```

### Adding a New API Endpoint

1. **Define Schema**

```python
# backend/app/schemas.py
class NewFeatureRequest(BaseModel):
    field1: str
    field2: int

class NewFeatureResponse(BaseModel):
    result: str
```

2. **Create Router**

```python
# backend/app/routers/new_feature.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import NewFeatureRequest, NewFeatureResponse

router = APIRouter(prefix="/api/new-feature", tags=["new-feature"])

@router.post("/", response_model=NewFeatureResponse)
async def create_new_feature(
    request: NewFeatureRequest,
    db: AsyncSession = Depends(get_db)
):
    # Implementation
    return NewFeatureResponse(result="success")
```

3. **Register Router**

```python
# backend/app/main.py
from app.routers import new_feature

app.include_router(new_feature.router)
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Agent service tests
cd agents_services
pytest

# Frontend tests
cd fair-hiring-frontend
npm test
```

---

## 12. Debugging Guide

### Common Issues

#### Issue 1: Database Connection Failed

**Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
1. Check PostgreSQL is running: `pg_isready`
2. Verify DATABASE_URL in `.env`
3. Check PostgreSQL logs: `tail -f /var/log/postgresql/postgresql-14-main.log`

#### Issue 2: Agent Service Not Responding

**Error:**
```
httpx.ConnectError: [Errno 111] Connection refused
```

**Solution:**
1. Check if service is running: `netstat -an | grep 8004`
2. Check service logs in terminal
3. Restart service: `python ats_service.py`

#### Issue 3: Frontend Can't Connect to Backend

**Error:**
```
CORS policy: No 'Access-Control-Allow-Origin' header
```

**Solution:**
1. Verify FRONTEND_URL in backend `.env`
2. Check CORS settings in `backend/app/main.py`
3. Ensure backend is running on correct port

#### Issue 4: Pipeline Stuck

**Symptoms:**
- Application status remains "pending"
- No credential generated

**Debug Steps:**
1. Check application status:
```sql
SELECT id, status, match_score FROM applications WHERE id = 42;
```

2. Check credential:
```sql
SELECT * FROM credentials WHERE application_id = 42;
```

3. Check agent service logs
4. Manually trigger pipeline:
```bash
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"application_id": 42}'
```

### Logging

**Backend Logs:**
```python
# backend/app/main.py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Application started")
logger.error(f"Error: {str(e)}")
```

**Agent Service Logs:**
```python
# agents_services/ats_service.py
logger = logging.getLogger("uvicorn.error")
logger.info("ATS analysis started")
```

### Database Debugging

```sql
-- Check recent applications
SELECT id, candidate_id, job_id, status, match_score, applied_at
FROM applications
ORDER BY applied_at DESC
LIMIT 10;

-- Check credentials
SELECT id, application_id, issued_at
FROM credentials
ORDER BY issued_at DESC
LIMIT 10;

-- Check review cases
SELECT id, application_id, triggered_by, severity, status
FROM review_cases
WHERE status = 'pending';

-- Check blacklist
SELECT id, candidate_id, reason, blacklisted_at
FROM blacklist
ORDER BY blacklisted_at DESC;
```

---

## 13. Known Issues

### Current Limitations

1. **Agent Services - Mock Logic**
   - `skill_agent_service.py` uses placeholder logic (TODO: integrate real agent)
   - `bias_agent_service.py` uses simple heuristics (TODO: integrate real agent)
   - `matching_agent_service.py` uses keyword matching (TODO: integrate real agent)

2. **Pipeline - Synchronous Execution**
   - Pipeline runs synchronously (blocks API response)
   - No background task queue (Celery not implemented)
   - Long-running pipelines may timeout

3. **Authentication - Basic Implementation**
   - No OAuth integration
   - No refresh tokens
   - No session management

4. **Error Handling - Limited Recovery**
   - Agent failures may leave pipeline in inconsistent state
   - No automatic retry mechanism
   - Limited error reporting to frontend

5. **Testing - Incomplete Coverage**
   - No unit tests for agent services
   - No integration tests for pipeline
   - No E2E tests

### Bugs to Fix

1. **ATS Service - Aggressive Blacklisting**
   - Issue: False positives in fraud detection
   - Impact: Legitimate resumes rejected
   - Status: Partially fixed (trust score threshold adjusted)

2. **GitHub Service - Rate Limiting**
   - Issue: Exceeds GitHub API rate limits
   - Impact: Service fails after ~50 requests
   - Workaround: Use personal access token

3. **Frontend - CORS Errors**
   - Issue: CORS mismatch between frontend and backend
   - Impact: API calls fail
   - Fix: Ensure FRONTEND_URL matches in backend `.env`

4. **Database - Missing Indexes**
   - Issue: Slow queries on large datasets
   - Impact: Performance degradation
   - Fix: Add indexes on frequently queried columns

---

## 14. Future Roadmap

### Phase 1: Complete Core Pipeline (Week 1-2)

- [ ] Integrate real agents into service wrappers
- [ ] Implement background task queue (Celery)
- [ ] Add pipeline retry mechanism
- [ ] Improve error handling and reporting

### Phase 2: Enhanced Features (Week 3-4)

- [ ] Add OAuth authentication (Google, GitHub)
- [ ] Implement refresh tokens
- [ ] Add real-time notifications (WebSockets)
- [ ] Create admin dashboard for review queue

### Phase 3: Scalability (Week 5-6)

- [ ] Add Redis caching layer
- [ ] Implement rate limiting
- [ ] Add monitoring (Prometheus/Grafana)
- [ ] Optimize database queries

### Phase 4: Testing & Quality (Week 7-8)

- [ ] Write unit tests (80% coverage)
- [ ] Write integration tests
- [ ] Write E2E tests
- [ ] Add CI/CD pipeline

### Phase 5: Production Deployment (Week 9-10)

- [ ] Dockerize all services
- [ ] Create Kubernetes manifests
- [ ] Set up staging environment
- [ ] Deploy to production
- [ ] Add SSL/TLS
- [ ] Configure CDN for frontend

---

## 15. Appendix

### A. File Structure

```
Agents-main/
├── agents_files/
│   └── Clean_Hiring_System/
│       ├── skill_verification_agent/
│       ├── bias_detection_agent/
│       ├── matching_agent/
│       └── ats_agent/
├── agents_services/
│   ├── ats_service.py
│   ├── github_service.py
│   ├── leetcode_service.py
│   ├── codeforces_service.py
│   ├── linkedin_service.py
│   ├── skill_agent_service.py
│   ├── conditional_test_service.py
│   ├── bias_agent_service.py
│   ├── matching_agent_service.py
│   ├── passport_service.py
│   ├── run_all_agents.py
│   ├── run_all_agents.bat
│   ├── requirements.txt
│   ├── README.md
│   ├── RUN_AGENTS_README.md
│   └── SETUP_GUIDE.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── passport.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── candidate.py
│   │   │   ├── company.py
│   │   │   ├── job.py
│   │   │   ├── application.py
│   │   │   └── pipeline.py
│   │   └── services/
│   │       ├── pipeline_service.py
│   │       └── agent_client.py
│   ├── uploads/
│   ├── requirements.txt
│   ├── .env
│   └── README.md
├── fair-hiring-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CandidateDashboard.jsx
│   │   │   ├── CompanyDashboard.jsx
│   │   │   ├── CompanyHiringFlow.jsx
│   │   │   ├── CompanyRolePipeline.jsx
│   │   │   ├── SkillPassport.jsx
│   │   │   └── JobPostingForm.jsx
│   │   ├── api/
│   │   │   └── client.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── README.md
├── SYSTEM_ANALYSIS_AND_GUIDE.md
├── SETUP_GUIDE.md
├── PROJECT_PRD.md (this file)
└── .env
```

### B. Port Mapping

| Service | Port | URL |
|---------|------|-----|
| Frontend | 5173 | http://localhost:5173 |
| Backend | 8000/8010 | http://localhost:8000 |
| Matching Agent | 8001 | http://localhost:8001 |
| Bias Agent | 8002 | http://localhost:8002 |
| Skill Agent | 8003 | http://localhost:8003 |
| ATS Agent | 8004 | http://localhost:8004 |
| GitHub Agent | 8005 | http://localhost:8005 |
| LeetCode Agent | 8006 | http://localhost:8006 |
| LinkedIn Agent | 8007 | http://localhost:8007 |
| Passport Agent | 8008 | http://localhost:8008 |
| Conditional Test | 8009 | http://localhost:8009 |
| Codeforces Agent | 8011 | http://localhost:8011 |
| PostgreSQL | 5432 | localhost:5432 |

### C. Key Contacts

- **Project Owner:** [Your Name]
- **Repository:** [Repository URL]
- **Documentation:** See `README.md` files in each directory

### D. Glossary

- **ATS:** Applicant Tracking System (fraud detection)
- **Anon ID:** Anonymous identifier for candidates
- **Credential:** Cryptographically signed skill passport
- **Ed25519:** Elliptic curve signature algorithm
- **Pipeline:** 10-stage verification workflow
- **Signal Strength:** Confidence level of skill verification

### E. Quick Commands Reference

```bash
# Start everything
cd agents_services && python run_all_agents.py &
cd backend && uvicorn app.main:app --reload &
cd fair-hiring-frontend && npm run dev &

# Stop everything
pkill -f "python.*service.py"
pkill -f uvicorn
pkill -f vite

# Database reset
dropdb fair_hiring && createdb fair_hiring
cd backend && python create_tables.py

# Check service health
for port in {8001..8011}; do curl -s http://localhost:$port/health | jq; done

# View logs
tail -f backend/logs/app.log
tail -f agents_services/logs/*.log
```

---

## For ChatGPT: How to Use This Document

### When Debugging

1. **Read the error message carefully**
2. **Check Section 12 (Debugging Guide)** for common issues
3. **Verify service status** using health check endpoints
4. **Check database state** using SQL queries in Section 12
5. **Review logs** from backend and agent services

### When Analyzing

1. **Understand architecture** from Section 3
2. **Review component interactions** from Section 4
3. **Check API contracts** in Section 7
4. **Understand pipeline flow** in Section 9

### When Developing

1. **Follow setup guide** in Section 10
2. **Use development guide** in Section 11
3. **Add tests** before implementing features
4. **Update this PRD** when making significant changes

### Key Files to Check

- **Backend entry point:** `backend/app/main.py`
- **Pipeline orchestrator:** `backend/app/services/pipeline_service.py`
- **Agent services:** `agents_services/*_service.py`
- **Database models:** `backend/app/models.py`
- **API schemas:** `backend/app/schemas.py`

---

**Document End**

*This PRD is a living document. Update it as the project evolves.*
