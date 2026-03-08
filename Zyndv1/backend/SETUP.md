# Fair Hiring Backend - Setup & Deployment Guide

## 📋 Prerequisites

Before setting up the backend, ensure you have:

1. **Python 3.10+** installed
2. **PostgreSQL 14+** installed and running
3. **Node.js 18+** (for frontend, if needed)
4. **Git** (for version control)

## 🚀 Quick Start

### 1. Database Setup

#### Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE fair_hiring_db;

# Exit
\q
```

#### Update Database Credentials

Edit `Agents-main/backend/.env` and update:

```env
DATABASE_URL=postgresql+asyncpg://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/fair_hiring_db
```

### 2. Backend Installation

```bash
# Navigate to backend directory
cd Agents-main/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Database Migrations

```bash
# Run Alembic migrations to create tables
alembic upgrade head
```

This will create all required tables:
- `candidates`
- `companies`
- `jobs`
- `applications`
- `credentials`
- `review_cases`

### 4. Start Agent Services

The backend requires all agent services to be running. Start them:

```bash
# Navigate to agents_services directory
cd ../agents_services

# Start all agent services (in separate terminals or use the start script)
python start_all_complete.py
```

# frontend
cd Agents-main\fair-hiring-frontend
npm run dev 

Or start each service individually:

```bash
# Terminal 1: ATS Service (port 8004)
python ats_service.py

# Terminal 2: GitHub Service (port 8005)
python github_service.py

# Terminal 3: LeetCode Service (port 8006)
python leetcode_service.py

# Terminal 4: LinkedIn Service (port 8007)
python linkedin_service.py

# Terminal 5: Skill Agent Service (port 8003)
python skill_agent_service.py

# Terminal 6: Bias Agent Service (port 8002)
python bias_agent_service.py

# Terminal 7: Matching Agent Service (port 8001)
python matching_agent_service.py

# Terminal 8: Passport Service (port 8008)
python passport_service.py
```

### 5. Start Backend Server

```bash
# Navigate back to backend directory
cd ../backend

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000`

### 6. Access API Documentation

Open your browser and navigate to:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Testing the Backend

### Run Test Script

```bash
# In the backend directory
python test_pipeline.py
```

This will:
1. Create a test candidate
2. Submit a test application
3. Run the full pipeline
4. Verify data is stored correctly
5. Display the generated credential

### Manual Testing with cURL

#### 1. Register a Candidate

```bash
curl -X POST "http://localhost:8000/api/candidates/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test Candidate",
    "gender": "prefer_not_to_say",
    "college": "MIT",
    "engineer_level": "Senior"
  }'
```

Response:
```json
{
  "id": 1,
  "anon_id": "ANON-ABC123",
  "email": "test@example.com",
  "name": "Test Candidate",
  "created_at": "2026-02-02T07:00:00Z"
}
```

#### 2. Submit Application

```bash
curl -X POST "http://localhost:8000/api/applications" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "resume_text": "Experienced software engineer with 5 years of experience...",
    "github_url": "https://github.com/example",
    "leetcode_url": "https://leetcode.com/example",
    "linkedin_url": "https://linkedin.com/in/example"
  }'
```

Response:
```json
{
  "application_id": 1,
  "status": "processing",
  "message": "Pipeline started in background"
}
```

#### 3. Check Application Status

```bash
curl "http://localhost:8000/api/applications/1"
```

#### 4. Get Candidate Passport

```bash
curl "http://localhost:8000/api/candidates/ANON-ABC123/passport"
```

## 📊 Database Verification

### Connect to Database

```bash
psql -U postgres -d fair_hiring_db
```

### Check Tables

```sql
-- List all tables
\dt

-- Check candidates
SELECT * FROM candidates;

-- Check applications
SELECT * FROM applications;

-- Check credentials
SELECT id, candidate_id, application_id, issued_at FROM credentials;

-- Check credential JSON
SELECT credential_json->>'candidate_name' as name, 
       credential_json->>'skill_confidence' as confidence
FROM credentials;
```

## 🔧 Configuration

### Environment Variables

Edit `Agents-main/backend/.env`:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fair_hiring_db

# JWT Secret (for future authentication)
JWT_SECRET=your-secret-key-change-in-production

# CORS Settings
CORS_ORIGINS=http://localhost:5173

# Agent Service URLs
ATS_SERVICE_URL=http://localhost:8004
GITHUB_SERVICE_URL=http://localhost:8005
LEETCODE_SERVICE_URL=http://localhost:8006
LINKEDIN_SERVICE_URL=http://localhost:8007
SKILL_SERVICE_URL=http://localhost:8003
BIAS_SERVICE_URL=http://localhost:8002
MATCHING_SERVICE_URL=http://localhost:8001
PASSPORT_SERVICE_URL=http://localhost:8008

# OpenAI API Key (for agents)
OPENAI_API_KEY=your-openai-api-key-here

# Application Settings
APP_NAME=Fair Hiring Backend
APP_VERSION=1.0.0
DEBUG=True
```

## 🐛 Troubleshooting

### Issue: Database Connection Failed

**Solution:**
1. Verify PostgreSQL is running: `pg_isready`
2. Check database exists: `psql -U postgres -l`
3. Verify credentials in `.env`
4. Check firewall settings

### Issue: Agent Services Not Responding

**Solution:**
1. Verify all agent services are running
2. Check ports are not in use: `netstat -an | findstr "8001"`
3. Check service logs for errors
4. Verify service URLs in `.env`

### Issue: Migration Failed

**Solution:**
```bash
# Rollback migration
alembic downgrade -1

# Check migration status
alembic current

# Re-run migration
alembic upgrade head
```

### Issue: CORS Errors

**Solution:**
1. Verify `CORS_ORIGINS` in `.env` matches frontend URL
2. Check frontend is running on correct port
3. Restart backend after changing `.env`

### Issue: Pipeline Timeout

**Solution:**
1. Check if all agent services are responsive
2. Increase timeout in `pipeline_service.py`
3. Check agent service logs for errors
4. Verify network connectivity between services

## 📝 API Endpoints Reference

### Candidate Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/candidates/register` | Register new candidate |
| POST | `/api/candidates/login` | Login candidate |
| GET | `/api/candidates/{anon_id}/stats` | Get candidate stats |
| GET | `/api/candidates/{anon_id}/applications` | Get candidate applications |
| GET | `/api/candidates/{anon_id}/passport` | Get candidate passport |

### Job Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs` | List published jobs |
| GET | `/api/jobs/{id}` | Get job details |
| POST | `/api/jobs` | Create new job (company) |

### Application Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/applications` | Submit application |
| GET | `/api/applications/{id}` | Get application details |
| PATCH | `/api/applications/{id}/status` | Update application status |

### Pipeline Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/pipeline/run` | Run full pipeline |

## 🚀 Production Deployment

### Using Docker (Recommended)

```bash
# Build Docker image
docker build -t fair-hiring-backend .

# Run container
docker run -d \
  --name fair-hiring-backend \
  -p 8000:8000 \
  --env-file .env \
  fair-hiring-backend
```

### Using Systemd (Linux)

Create `/etc/systemd/system/fair-hiring-backend.service`:

```ini
[Unit]
Description=Fair Hiring Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/Agents-main/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl enable fair-hiring-backend
sudo systemctl start fair-hiring-backend
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in the terminal
3. Check agent service logs
4. Verify database state
5. Contact development team

## 📄 License

This project is part of the Fair Hiring System.