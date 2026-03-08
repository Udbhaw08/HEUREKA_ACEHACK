"""
Check Skill Verification Agent results from database
"""
import asyncio
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from sqlalchemy import text

async def check_skill_results(application_id: int):
    """Check what the Skill Verification Agent evaluated"""
    
    async for db in get_db():
        # Get skill agent run
        query = text("""
            SELECT 
                agent_name,
                status,
                output_payload,
                created_at
            FROM agent_runs 
            WHERE application_id = :app_id 
            AND agent_name = 'skill'
            ORDER BY created_at DESC
            LIMIT 1
        """)
        
        result = await db.execute(query, {"app_id": application_id})
        row = result.fetchone()
        
        if not row:
            print(f"❌ No Skill Agent results found for application {application_id}")
            return
        
        agent_name = row[0]
        status = row[1]
        output = row[2]
        created_at = row[3]
        
        print("=" * 70)
        print(f"SKILL VERIFICATION AGENT RESULTS - APPLICATION {application_id}")
        print("=" * 70)
        print(f"Status: {status}")
        print(f"Processed: {created_at}")
        
        # Extract key information
        data = output if isinstance(output, dict) else {}
        
        print(f"\n🎯 SKILL EVALUATION SUMMARY:")
        print(f"  Credential ID: {data.get('credential_id', 'N/A')}")
        print(f"  Evaluation ID: {data.get('evaluation_id', 'N/A')}")
        print(f"  Skill Confidence: {data.get('skill_confidence', 0)}%")
        print(f"  Signal Strength: {data.get('signal_strength', 'N/A')}")
        print(f"  Credential Status: {data.get('credential_status', 'N/A')}")
        print(f"  Test Required: {data.get('test_required', False)}")
        print(f"  Next Stage: {data.get('next_stage', 'N/A')}")
        
        print(f"\n✅ VERIFIED SKILLS:")
        verified_skills = data.get('verified_skills', {})
        if verified_skills:
            for category, skills in verified_skills.items():
                if skills:
                    print(f"\n  {category.upper()}:")
                    if isinstance(skills, list):
                        for skill in skills:
                            print(f"    • {skill}")
                    elif isinstance(skills, dict):
                        for skill, details in skills.items():
                            print(f"    • {skill}: {details}")
        else:
            print("  No verified skills found")
        
        print(f"\n📊 EVIDENCE SUMMARY:")
        evidence = data.get('evidence_summary', {})
        if evidence:
            for source, info in evidence.items():
                print(f"\n  {source.upper()}:")
                if isinstance(info, dict):
                    for key, value in info.items():
                        print(f"    {key}: {value}")
                else:
                    print(f"    {info}")
        else:
            print("  No evidence summary available")
        
        print(f"\n💡 CONFIDENCE EXPLANATION:")
        explanation = data.get('confidence_explanation', 'N/A')
        print(f"  {explanation}")
        
        print(f"\n📋 FULL OUTPUT:")
        print(json.dumps(output, indent=2))
        
        break

if __name__ == "__main__":
    app_id = int(sys.argv[1]) if len(sys.argv) > 1 else 35
    asyncio.run(check_skill_results(app_id))
