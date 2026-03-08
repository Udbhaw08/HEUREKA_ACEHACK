# 🚀 Quick Start Guide - Fair Hiring Backend

This guide will help you get the Fair Hiring Backend up and running in **5 minutes**.

## ⚡ Prerequisites Check

Before starting, ensure you have:

- [ ] Python 3.10+ installed
- [ ] PostgreSQL 14+ installed and running
- [ ] Git (optional)

## 📝 Step-by-Step Setup

### Step 1: Create PostgreSQL Database

Open a terminal and run:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE fair_hiring_db;

# Exit
\q
```

### Step 2: Navigate to Backend Directory

```bash
cd Agents-main/backend
```

### Step 3: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run Database Migrations

```bash
alembic upgrade head
```

You should see output like:
```
Running upgrade  -> 001
```

### Step 6: Start Agent Services

Open a **new terminal** and run:

```bash
cd Agents-main/agents_services
python start_all_complete.py
```

This will start all 8 agent services on ports 8001-8008.

### Step 7: Start Backend Server

Open another **new terminal** and run:

```bash
cd Agents-main/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 8: Verify Backend is Running

Open your browser and navigate to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You should see the API documentation with all endpoints listed.

## 🧪 Test the Backend

### Option 1: Run Automated Test Script

In a **new terminal**, run:

```bash
cd Agents-main/backend
python test_pipeline.py
```

This will:
1. Create a test candidate
2. Create a test job
3. Submit an application
4. Run the full pipeline
5. Display the generated credential

### Option 2: Manual Test with cURL

#### Register a Candidate

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

#### Submit an Application

```bash
curl -X POST "http://localhost:8000/api/applications" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "resume_text": "Experienced software engineer with 5 years of experience in Python and JavaScript...",
    "github_url": "https://github.com/example",
    "leetcode_url": "https://leetcode.com/example",
    "linkedin_url": "https://linkedin.com/in/example"
  }'
```

#### Get Candidate Passport

```bash
curl "http://localhost:8000/api/candidates/ANON-ABC123/passport"
```

## ✅ Success Indicators

You know everything is working if:

1. ✅ All agent services started without errors
2. ✅ Backend server is running on port 8000
3. ✅ You can access Swagger UI at http://localhost:8000/docs
4. ✅ Database tables were created (check with `\dt` in psql)
5. ✅ Test script completed successfully
6. ✅ You can fetch a passport from the API

## 🔍 Troubleshooting

### Issue: "Database connection failed"

**Solution:**
1. Verify PostgreSQL is running: `pg_isready`
2. Check database exists: `psql -U postgres -l`
3. Update credentials in `.env` file

### Issue: "Agent service not responding"

**Solution:**
1. Check if agent services are running
2. Verify ports are not in use: `netstat -an | findstr "8001"`
3. Check agent service logs for errors

### Issue: "Migration failed"

**Solution:**
```bash
# Rollback and retry
alembic downgrade -1
alembic upgrade head
```

### Issue: "CORS error in browser"

**Solution:**
1. Check `CORS_ORIGINS` in `.env` matches frontend URL
2. Restart backend after changing `.env`

## 📊 Verify Database

Connect to PostgreSQL and check tables:

```bash
psql -U postgres -d fair_hiring_db

# List tables
\dt

# Check candidates
SELECT * FROM candidates;

# Check applications
SELECT * FROM applications;

# Check credentials
SELECT id, candidate_id, application_id, issued_at FROM credentials;

# Exit
\q
```

## 🎯 Next Steps

### For Development

1. **Start Frontend**:
   ```bash
   cd Agents-main/fair-hiring-frontend
   npm install
   npm run dev
   ```

2. **Test Full Integration**:
   - Open frontend at http://localhost:5173
   - Register a candidate
   - Apply to a job
   - View the skill passport

### For Production

1. **Update `.env`** with production credentials
2. **Set up SSL/HTTPS**
3. **Configure firewall rules**
4. **Set up database backups**
5. **Deploy with Docker** (see SETUP.md)

## 📚 Additional Documentation

- **SETUP.md** - Complete setup and deployment guide
- **README.md** - Project overview
- **BACKEND_REBUILD_SUMMARY.md** - Detailed architecture documentation
- **API Docs** - http://localhost:8000/docs

## 🆘 Need Help?

1. Check the troubleshooting section above
2. Review logs in the terminal
3. Check agent service logs
4. Verify database state
5. Read SETUP.md for detailed instructions

## 🎉 You're Ready!

The Fair Hiring Backend is now running and ready to:
- ✅ Accept candidate registrations
- ✅ Process job applications
- ✅ Run AI agent pipelines
- ✅ Generate skill passports
- ✅ Store all data in PostgreSQL

**Start building your fair hiring platform!** 🚀