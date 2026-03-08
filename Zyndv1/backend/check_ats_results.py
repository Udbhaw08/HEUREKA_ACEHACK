"""
Check ATS extraction results from database
"""
import asyncio
import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from sqlalchemy import text

async def check_ats_results(application_id: int):
    """Check what ATS extracted for an application"""
    
    async for db in get_db():
        # Get ATS agent run
        query = text("""
            SELECT 
                agent_name,
                status,
                output_payload,
                created_at
            FROM agent_runs 
            WHERE application_id = :app_id 
            AND agent_name = 'ats'
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        
        result = await db.execute(query, {"app_id": application_id})
        row = result.fetchone()
        
        if not row:
            print(f"❌ No ATS results found for application {application_id}")
            return
        
        print("=" * 70)
        print(f"ATS RESULTS FOR APPLICATION {application_id}")
        print("=" * 70)
        
        print(f"\n📊 Status: {row[1]}")
        print(f"⏰ Processed: {row[3]}")
        
        output = row[2]
        
        print("\n🔍 ATS Analysis:")
        print(f"  Action: {output.get('action')}")
        print(f"  Fraud Detected: {output.get('fraud_detected')}")
        print(f"  Manipulation Detected: {output.get('manipulation_detected')}")
        
        # Check for production fields
        signals = output.get('manipulation_signals', {})
        print(f"\n🛡️ Security Signals:")
        print(f"  Trust Score: {signals.get('trust_score')} (0-100)")
        print(f"  Confidence: {signals.get('confidence')} (0.0-1.0)")
        print(f"  Guard Version: {signals.get('guard_version')}")
        print(f"  Patterns: {signals.get('patterns', [])}")
        
        # Evidence extracted
        evidence = output.get('evidence', {})
        if evidence:
            print(f"\n📄 Evidence Extracted:")
            
            identity = evidence.get('identity', {})
            print(f"  Name: {identity.get('name', 'N/A')}")
            
            skills = evidence.get('skills', [])
            if skills:
                print(f"  Skills: {', '.join([s.get('skill', '') for s in skills[:10]])}")
            
            experience = evidence.get('experience', [])
            if experience:
                print(f"  Experience: {len(experience)} entries")
                for exp in experience[:3]:
                    print(f"    - {exp.get('role', 'N/A')} at {exp.get('company', 'N/A')}")
            
            projects = evidence.get('projects', [])
            if projects:
                print(f"  Projects: {len(projects)} projects")
        
        # Full output (optional)
        print(f"\n📋 Full Output (JSON):")
        print(json.dumps(output, indent=2))
        
        break

if __name__ == "__main__":
    app_id = int(sys.argv[1]) if len(sys.argv) > 1 else 29
    asyncio.run(check_ats_results(app_id))
