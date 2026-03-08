import asyncio
import os
import sys
from pathlib import Path
from sqlalchemy import select, update

# Add parent directory to sys.path to allow imports from app
sys.path.append(str(Path(__file__).resolve().parent))

from app.database import engine
from app.models import Job
from app.agents.job_extraction import JobExtractionAgent

async def verify_extraction(job_id: int, update_db: bool = False):
    async with engine.connect() as conn:
        # 1. Fetch Job
        q = await conn.execute(select(Job).where(Job.id == job_id))
        job = q.fetchone()
        
        if not job:
            print(f"Error: Job {job_id} not found.")
            return

        print(f"--- VERIFYING EXTRACTION FOR JOB {job_id} ---")
        print(f"Title: {job.title}")
        print(f"Current Skills in DB: {job.required_skills}")
        
        # 2. Run Extraction Agent
        agent = JobExtractionAgent()
        result = agent.extract(job.description, title=job.title)
        
        print("\n--- AGENT OUTPUT ---")
        print(f"Role: {result.get('role', 'N/A')}")
        print(f"Seniority: {result.get('seniority', 'N/A')}")
        print(f"Core Skills: {result.get('core_skills', [])}")
        print(f"Frameworks: {result.get('frameworks', [])}")
        print(f"Evidence Signals: {result.get('evaluation_signals', {})}")
        print(f"Exclusions: {result.get('excluded_signals', [])}")
        
        # 3. Update DB if requested
        if update_db and result.get('core_skills'):
            print("\nUpdating database with full semantic spec...")
            await conn.execute(
                update(Job)
                .where(Job.id == job_id)
                .values(required_skills=result) # Save the WHOLE dict
            )
            await conn.commit()
            print("Database updated successfully.")

if __name__ == "__main__":
    job_target = 3
    # First run without update to show the user
    asyncio.run(verify_extraction(job_target, update_db=True))
