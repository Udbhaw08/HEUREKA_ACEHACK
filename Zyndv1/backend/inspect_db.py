
import asyncio
import os
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:1234@localhost:5432/fair_hiring"
)

async def inspect_db():
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
    
    # Import models at runtime to avoid circular imports
    import sys
    sys.path.append(os.getcwd())
    from app.models import Candidate, Job, Application, Credential
    
    async with AsyncSessionLocal() as session:
        print("\n=== LATEST CANDIDATES ===")
        candidates = (await session.execute(select(Candidate).order_by(Candidate.id.desc()).limit(3))).scalars().all()
        for c in candidates:
            print(f"ID: {c.id}, Name: {c.name}, Email: {c.email}, Created: {c.created_at}")
            
        print("\n=== LATEST JOBS ===")
        jobs = (await session.execute(select(Job).order_by(Job.id.desc()).limit(3))).scalars().all()
        for j in jobs:
            print(f"ID: {j.id}, Title: {j.title}")
            print(f"  Reqs: {json.dumps(j.required_skills, indent=2)}")
            
        print("\n=== LATEST APPLICATIONS ===")
        apps = (await session.execute(select(Application).order_by(Application.id.desc()).limit(3))).scalars().all()
        for a in apps:
            print(f"ID: {a.id}, Candidate: {a.candidate_id}, Job: {a.job_id}, Status: {a.pipeline_status}, Score: {a.match_score}, Created: {a.created_at}")
            if a.pipeline_error:
                print(f"  Error: {a.pipeline_error}")
            
        print("\n=== LATEST CREDENTIALS ===")
        creds = (await session.execute(select(Credential).order_by(Credential.id.desc()).limit(3))).scalars().all()
        for cr in creds:
            print(f"ID: {cr.id}, App ID: {cr.application_id}, Issued: {cr.issued_at}")
            print(f"  Hash: {cr.hash_sha256[:10]}...")
            print(f"  Signature: {cr.signature_b64[:20]}...")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(inspect_db())
