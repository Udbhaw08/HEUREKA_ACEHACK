"""
Check LinkedIn PDF extraction results from database
"""
import asyncio
import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from sqlalchemy import text

async def check_linkedin_results(application_id: int):
    """Check what LinkedIn agent extracted"""
    
    async for db in get_db():
        # Get LinkedIn agent run
        query = text("""
            SELECT 
                agent_name,
                status,
                output_payload,
                created_at
            FROM agent_runs 
            WHERE application_id = :app_id 
            AND agent_name = 'linkedin'
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        
        result = await db.execute(query, {"app_id": application_id})
        row = result.fetchone()
        
        if not row:
            print(f"❌ No LinkedIn results found for application {application_id}")
            return
        
        print("=" * 70)
        print(f"LINKEDIN RESULTS FOR APPLICATION {application_id}")
        print("=" * 70)
        
        print(f"\n📊 Status: {row[1]}")
        print(f"⏰ Processed: {row[3]}")
        
        output = row[2]
        
        print("\n🔍 LinkedIn Analysis:")
        print(f"  Success: {output.get('success')}")
        
        data = output.get('data', {})
        
        # Identity
        identity = data.get('identity', {})
        if identity:
            print(f"\n👤 Identity:")
            print(f"  Name: {identity.get('name', 'N/A')}")
            print(f"  Email: {identity.get('email', 'N/A')}")
            print(f"  Location: {identity.get('location', 'N/A')}")
        
        # Experience
        experience = data.get('experience', [])
        if experience:
            print(f"\n💼 Experience ({len(experience)} entries):")
            for exp in experience[:5]:
                print(f"  - {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
                print(f"    Duration: {exp.get('duration', 'N/A')}")
        
        # Education
        education = data.get('education', [])
        if education:
            print(f"\n🎓 Education ({len(education)} entries):")
            for edu in education[:3]:
                print(f"  - {edu.get('degree', 'N/A')} from {edu.get('institution', 'N/A')}")
        
        # Skills
        skills = data.get('skills', [])
        if skills:
            print(f"\n🛠️ Skills:")
            print(f"  {', '.join(skills[:20])}")
        
        # Signals
        profile_signals = data.get('profile_signals', {})
        if profile_signals:
            print(f"\n📈 Profile Signals:")
            print(f"  Confidence Score: {profile_signals.get('confidence_score', 'N/A')}")
        
        # Full output
        print(f"\n📋 Full Output (JSON):")
        print(json.dumps(output, indent=2))
        
        break

if __name__ == "__main__":
    app_id = int(sys.argv[1]) if len(sys.argv) > 1 else 31
    asyncio.run(check_linkedin_results(app_id))
