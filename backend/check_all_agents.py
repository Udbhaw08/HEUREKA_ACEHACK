"""
Comprehensive check of all agent results for an application
"""
import asyncio
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from sqlalchemy import text

async def check_all_agents(application_id: int):
    """Check all agent results for an application"""
    
    async for db in get_db():
        query = text("""
            SELECT 
                agent_name,
                status,
                output_payload
            FROM agent_runs 
            WHERE application_id = :app_id 
            ORDER BY agent_name
        """)
        
        result = await db.execute(query, {"app_id": application_id})
        rows = result.fetchall()
        
        if not rows:
            print(f"❌ No agent results found for application {application_id}")
            return
        
        print("=" * 80)
        print(f"ALL AGENT RESULTS - APPLICATION {application_id}")
        print("=" * 80)
        
        for row in rows:
            agent_name = row[0]
            status = row[1]
            output = row[2]
            
            print(f"\n{'='*80}")
            print(f"📊 {agent_name.upper()} AGENT")
            print(f"{'='*80}")
            print(f"Status: {status}")
            
            # Check if output is empty or has data
            has_data = False
            if isinstance(output, dict):
                # Check for non-empty values
                for key, value in output.items():
                    if value:  # Not None, not empty string, not empty list/dict
                        if isinstance(value, (list, dict)):
                            if len(value) > 0:
                                has_data = True
                                break
                        else:
                            has_data = True
                            break
            
            if has_data:
                print("✅ Has data")
                print(f"\nKey fields:")
                for key, value in list(output.items())[:5]:  # Show first 5 fields
                    if isinstance(value, (list, dict)):
                        print(f"  {key}: {type(value).__name__} with {len(value)} items")
                    else:
                        print(f"  {key}: {value}")
            else:
                print("⚠️  EMPTY OUTPUT - No meaningful data")
            
            print(f"\nFull output:")
            print(json.dumps(output, indent=2)[:500] + "..." if len(json.dumps(output)) > 500 else json.dumps(output, indent=2))
        
        break

if __name__ == "__main__":
    app_id = int(sys.argv[1]) if len(sys.argv) > 1 else 35
    asyncio.run(check_all_agents(app_id))
