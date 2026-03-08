import asyncio
import os
import sys

# Add backend to path to import models
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_path)
os.chdir(backend_path)  # Ensure .env is loaded from backend directory

from app.db import SessionLocal
from app.models import Application, Credential, Candidate, AgentRun, ReviewCase, Blacklist, LogEntry
from sqlalchemy import delete

async def reset_db():
    async with SessionLocal() as db:
        print("Resetting database mock data...")
        
        # We delete in order of dependencies
        await db.execute(delete(LogEntry))
        await db.execute(delete(ReviewCase))
        await db.execute(delete(Blacklist))
        await db.execute(delete(AgentRun))
        await db.execute(delete(Credential))
        await db.execute(delete(Application))
        
        # Optionally delete candidates if they are just for tests
        # await db.execute(delete(Candidate))
        
        await db.commit()
        print("Database reset complete. (Kept Companies, Jobs, and Candidates for now)")

if __name__ == "__main__":
    asyncio.run(reset_db())
