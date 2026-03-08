import asyncio
import os
import sys
from pathlib import Path
from sqlalchemy import select

# Add parent directory to sys.path to allow imports from app
sys.path.append(str(Path(__file__).resolve().parent))

from app.database import engine
from app.models import Job, Application, Candidate, Company

async def inspect_db():
    async with engine.connect() as conn:
        print("--- COMPANIES ---")
        q = await conn.execute(select(Company.id, Company.name))
        for row in q.all():
            print(f"ID: {row.id} (type: {type(row.id)}), Name: {row.name}")

        print("\n--- JOBS ---")
        q = await conn.execute(select(Job.id, Job.title, Job.company_id, Job.required_skills, Job.description))
        for row in q.all():
            print(f"ID: {row.id}, Title: {row.title}")
            print(f"   Skills: {row.required_skills}")
            if row.id == 3:
                print(f"   Description: {row.description}")
                print(f"   Full JD Length: {len(row.description)} chars")

        print("\n--- APPLICATIONS ---")
        q = await conn.execute(select(Application.id, Application.job_id, Application.status, Application.candidate_id))
        for row in q.all():
            print(f"ID: {row.id}, Job ID: {row.job_id}, Status: {row.status}, Candidate ID: {row.candidate_id}")

        print("\n--- CANDIDATES ---")
        q = await conn.execute(select(Candidate.id, Candidate.anon_id))
        for row in q.all():
            print(f"ID: {row.id}, Anon ID: {row.anon_id}")

if __name__ == "__main__":
    asyncio.run(inspect_db())
