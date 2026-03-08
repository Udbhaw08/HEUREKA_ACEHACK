"""
Check what job data is being sent to matching service
"""
import asyncio
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from sqlalchemy import text

async def check_job_data():
    """Check the latest job's required_skills structure"""
    
    async for db in get_db():
        # Get the latest job
        query = text("""
            SELECT 
                id,
                title,
                description,
                required_skills,
                company_id
            FROM jobs 
            ORDER BY id DESC 
            LIMIT 1
        """)
        
        result = await db.execute(query)
        row = result.fetchone()
        
        if not row:
            print("❌ No jobs found in database")
            return
        
        job_id = row[0]
        title = row[1]
        description = row[2]
        required_skills = row[3]
        company_id = row[4]
        
        print("=" * 70)
        print(f"LATEST JOB DATA (ID: {job_id})")
        print("=" * 70)
        print(f"\n📋 Title: {title}")
        print(f"🏢 Company ID: {company_id}")
        print(f"\n📝 Description (first 200 chars):")
        print(f"{description[:200]}...")
        
        print(f"\n🔧 Required Skills:")
        print(f"  Type: {type(required_skills)}")
        print(f"  Value: {json.dumps(required_skills, indent=2)}")
        
        # Simulate what pipeline_service does
        print(f"\n🔄 SIMULATING PIPELINE DATA PREPARATION:")
        print("=" * 70)
        
        if isinstance(required_skills, dict):
            print("✅ required_skills is a dict")
            data = required_skills.copy()
            languages = data.get("languages", []) if isinstance(data.get("languages"), list) else []
            
            data.update({
                "title": title,
                "description": description,
                "company_id": company_id,
                "languages": languages,
                "matching_philosophy": "skills_based"
            })
            
            print(f"\n📤 Data that would be sent to matching service:")
            print(json.dumps(data, indent=2))
            
            # Check required fields
            print(f"\n✅ Required fields check:")
            print(f"  - strict_requirements: {'✅' if 'strict_requirements' in data else '❌ MISSING'}")
            print(f"  - languages: {'✅' if 'languages' in data else '❌ MISSING'}")
            print(f"  - matching_philosophy: {'✅' if 'matching_philosophy' in data else '❌ MISSING'}")
            
        else:
            print(f"❌ required_skills is NOT a dict, it's a {type(required_skills)}")
            print(f"   This will cause the matching service to fail!")
        
        break

if __name__ == "__main__":
    asyncio.run(check_job_data())
