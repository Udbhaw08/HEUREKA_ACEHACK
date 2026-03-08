
import asyncio
import os
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import selectinload
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:1234@localhost:5432/fair_hiring"
)

async def deep_dive(anon_id_query: str):
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
    
    import sys
    sys.path.append(os.getcwd())
    from app.models import Candidate, Application, AgentRun, Credential
    
    async with AsyncSessionLocal() as session:
        print(f"\n🔍 Searching for Anon ID: {anon_id_query}")
        
        # Find candidate
        stmt = select(Candidate).where(Candidate.anon_id.ilike(f"%{anon_id_query}%"))
        candidate = (await session.execute(stmt)).scalars().first()
        
        if not candidate:
            print("❌ Candidate not found.")
            return

        print(f"\n✅ FOUND: Candidate ID {candidate.id}")
        print(f"Name Overlay: {candidate.name}")
        print(f"Anon ID: {candidate.anon_id}")
        
        # Find applications
        stmt = select(Application).where(Application.candidate_id == candidate.id).order_by(Application.id.desc())
        apps = (await session.execute(stmt)).scalars().all()
        
        for app in apps:
            print(f"\n--- Application ID: {app.id} ---")
            print(f"Status: {app.pipeline_status}")
            print(f"Match Score: {app.match_score}")
            
            # Find Agent Runs
            stmt = select(AgentRun).where(AgentRun.application_id == app.id).order_by(AgentRun.id)
            runs = (await session.execute(stmt)).scalars().all()
            
            print("\n🤖 AGENT RUNS:")
            for run in runs:
                print(f"  - {run.agent_name}: {run.status}")
                if run.output_payload:
                    print(f"    Output: {json.dumps(run.output_payload, indent=2)[:500]}...")
                if run.error_message:
                    print(f"    Error: {run.error_message}")
            
            # Find Credential
            stmt = select(Credential).where(Credential.application_id == app.id)
            cred = (await session.execute(stmt)).scalars().first()
            if cred:
                print("\n📜 CREDENTIAL:")
                print(json.dumps(cred.credential_json, indent=2))
                print(f"Signature: {cred.signature_b64[:30]}...")
            else:
                print("\n⚠️ No credential issued yet.")

    await engine.dispose()

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "ANON-6CB1C034FF97"
    asyncio.run(deep_dive(query))
