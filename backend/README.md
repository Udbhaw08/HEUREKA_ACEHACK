# Fair Hiring System Backend API

## Overview

This is the backend API for the Fair Hiring Platform - an AI-powered skill verification and bias-free recruitment system. The backend orchestrates multiple AI agents to analyze candidate profiles, verify skills, and generate cryptographically signed skill passports.

## Architecture

### Components

1. **FastAPI Application** - RESTful API server
2. **PostgreSQL Database** - Persistent storage with asyncpg
3. **Agent Services** - 8 independent AI agents running on separate ports
4. **Pipeline Orchestrator** - Coordinates agent execution
5. **Background Task System** - Async processing of long-running pipelines

### Agent Services

| Service | Port | Purpose |
|---------|------|---------|
| ATS Agent | 8004 | Resume fraud detection |
| GitHub Agent | 8005 | Code repository analysis |
| LeetCode Agent | 8006 | Algorithmic problem solving verification |
| LinkedIn Agent | 8007 | Professional history verification |
| Skill Agent | 8003 | Skill verification and evidence graph |
| Bias Agent | 8002 | Bias detection in job descriptions |
| Matching Agent | 8001 | Candidate-job matching |
| Passport Agent | 8008 | Credential generation and signing |

## Database Schema

### Tables

1. **candidates** - Candidate profiles and authentication
2. **jobs** - Job postings with fairness scores
3. **applications** - Job applications with pipeline results
4. **credentials** - Skill passports with cryptographic signatures
5. **review_cases** - Human review queue for flagged applications

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Node.js 18+ (for frontend)

### 1. Install Dependencies

```bash
cd Agents-main/backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# - Update DATABASE_URL with your PostgreSQL credentials
# - Update agent service URLs if needed
```

### 3. Initialize Database

```bash
# Create PostgreSQL database
createdb fair_hiring

# Run migrations
alembic upgrade head
```

### 4. Start Agent Services

In a separate terminal:

```bash
cd Agents-main/agents_services
python start_all.py
```

This will start all 8 agent services on their respective ports.

### 5. Start Backend Server

```bash
cd Agents-main/backend
python -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /health` - Health check
- `GET /` - API information

### Candidate APIs
- `POST /api/candidates/register` - Register new candidate
- `POST /api/candidates/login` - Login candidate
- `GET /api/candidates/{anon_id}/stats` - Get candidate statistics
- `GET /api/candidates/{anon_id}/applications` - Get candidate applications
- `GET /api/candidates/{anon_id}/passport` - Get candidate's skill passport

### Job APIs
- `GET /api/jobs` - List all published jobs
- `GET /api/jobs/{id}` - Get job details
- `POST /api/jobs` - Create new job (company)

### Application APIs
- `POST /api/applications` - Submit job application
- `GET /api/applications/{id}` - Get application details
- `PATCH /api/applications/{id}/status` - Update application status

### Pipeline APIs
- `POST /api/pipeline/run` - Run full analysis pipeline
- `GET /api/pipeline/status/{application_id}` - Get pipeline status
- `GET /api/pipeline/result/{application_id}` - Get pipeline results

## Pipeline Execution Flow

The `/api/pipeline/run` endpoint orchestrates the following sequence:

1. **ATS Analysis** - Detect resume fraud and extract skills
2. **GitHub Scraping** - Analyze code repositories
3. **LeetCode Verification** - Verify algorithmic skills
4. **LinkedIn Verification** - Verify professional history
5. **Skill Verification** - Build evidence graph for skills
6. **Bias Detection** - Check for bias in evaluation
7. **Matching** - Calculate match score with job requirements
8. **Passport Generation** - Create signed credential

All results are aggregated and stored in the database.

## Testing

### Run Test Script

```bash
cd Agents-main/backend
python test_pipeline.py
```

This will:
1. Create a test candidate
2. Submit a test application
3. Run the full pipeline
4. Verify data persistence
5. Display the generated credential

### Manual Testing with Swagger

1. Open http://localhost:8000/docs
2. Register a candidate via `/api/candidates/register`
3. Create a job via `/api/jobs` (or use existing)
4. Submit application via `/api/applications`
5. Run pipeline via `/api/pipeline/run`
6. Check results via `/api/pipeline/result/{application_id}`

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── agent_client.py      # Agent service client
│   ├── routers/
│   │   ├── pipeline.py      # Pipeline endpoints
│   │   ├── candidate.py     # Candidate endpoints
│   │   ├── job.py           # Job endpoints
│   │   └── application.py   # Application endpoints
│   └── services/
│       └── pipeline_service.py  # Pipeline orchestrator
├── alembic/                 # Database migrations
├── uploads/                 # File uploads
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | - |
| FRONTEND_URL | Frontend URL for CORS | http://localhost:5173 |
| ATS_SERVICE_URL | ATS agent URL | http://localhost:8004 |
| GITHUB_SERVICE_URL | GitHub agent URL | http://localhost:8005 |
| LEETCODE_SERVICE_URL | LeetCode agent URL | http://localhost:8006 |
| LINKEDIN_SERVICE_URL | LinkedIn agent URL | http://localhost:8007 |
| SKILL_SERVICE_URL | Skill agent URL | http://localhost:8003 |
| BIAS_SERVICE_URL | Bias agent URL | http://localhost:8002 |
| MATCHING_SERVICE_URL | Matching agent URL | http://localhost:8001 |
| PASSPORT_SERVICE_URL | Passport agent URL | http://localhost:8008 |
| AGENT_TIMEOUT | Agent timeout in seconds | 60 |
| DEBUG | Debug mode | true |

## Common Issues

### Database Connection Failed

1. Ensure PostgreSQL is running
2. Check DATABASE_URL in .env
3. Verify database exists: `psql -l`

### Agent Services Not Responding

1. Check if agent services are running: `netstat -an | grep 800[1-8]`
2. Check agent service logs
3. Verify agent service URLs in .env

### Pipeline Timeout

1. Increase AGENT_TIMEOUT in .env
2. Check if agent services are processing requests
3. Review agent service logs for errors

### CORS Errors

1. Verify FRONTEND_URL matches your frontend URL
2. Check browser console for specific error
3. Ensure backend is running on correct port

## Development

### Adding New Endpoints

1. Create schema in `app/schemas.py`
2. Add route handler in `app/routers/`
3. Register router in `app/main.py`
4. Test with Swagger UI

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## Production Deployment

### Security Checklist

- [ ] Change SECRET_KEY in .env
- [ ] Set DEBUG=false
- [ ] Use strong database password
- [ ] Enable HTTPS
- [ ] Configure firewall rules
- [ ] Set up database backups
- [ ] Enable request logging
- [ ] Configure rate limiting

### Docker Deployment

```bash
# Build image
docker build -t fair-hiring-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/fair_hiring \
  fair-hiring-backend
```

## Support

For issues and questions:
1. Check the logs in the terminal
2. Review Swagger documentation at /docs
3. Check agent service logs
4. Verify database connection

## License

Proprietary - Fair Hiring System