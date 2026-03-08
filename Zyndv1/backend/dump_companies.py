import asyncio
from app.db import async_session_maker
from app.models import Company, Job
from sqlalchemy import select

async def dump_companies():
    print("Dumping companies...")
    async with async_session_maker() as db:
        q = await db.execute(select(Company))
        companies = q.scalars().all()
        for c in companies:
            print(f"ID: {c.id}, Name: {c.name}, Email: {c.email}")
            
            # Jobs
            q_job = await db.execute(select(Job).where(Job.company_id == c.id))
            jobs = q_job.scalars().all()
            for j in jobs:
                print(f"  Job ID: {j.id}, Title: {j.title}, Published: {j.published}")
    print("Done.")

if __name__ == "__main__":
    asyncio.run(dump_companies())
