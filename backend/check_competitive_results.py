"""
Check LeetCode and Codeforces extraction results from database
"""
import asyncio
import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from sqlalchemy import text

async def check_competitive_results(application_id: int):
    """Check what LeetCode and Codeforces agents extracted"""
    
    async for db in get_db():
        # Get both agent runs
        query = text("""
            SELECT 
                agent_name,
                status,
                output_payload,
                created_at
            FROM agent_runs 
            WHERE application_id = :app_id 
            AND agent_name IN ('leetcode', 'codeforces')
            ORDER BY agent_name, created_at DESC
        """)
        
        result = await db.execute(query, {"app_id": application_id})
        rows = result.fetchall()
        
        if not rows:
            print(f"❌ No LeetCode/Codeforces results found for application {application_id}")
            return
        
        print("=" * 70)
        print(f"COMPETITIVE PROGRAMMING RESULTS FOR APPLICATION {application_id}")
        print("=" * 70)
        
        for row in rows:
            agent_name = row[0]
            status = row[1]
            output = row[2]
            created_at = row[3]
            
            print(f"\n{'='*70}")
            print(f"📊 {agent_name.upper()} RESULTS")
            print(f"{'='*70}")
            print(f"Status: {status}")
            print(f"Processed: {created_at}")
            
            if agent_name == 'leetcode':
                print(f"\n🔢 LeetCode Stats:")
                # Try nested data first, then root level
                data = output.get('data', output)
                print(f"  Username: {data.get('username', 'N/A')}")
                print(f"  Total Solved: {data.get('total_solved', 0)}")
                print(f"  Ranking: {data.get('ranking', 'N/A')}")
                print(f"  Easy: {data.get('easy_solved', 0)}")
                print(f"  Medium: {data.get('medium_solved', 0)}")
                print(f"  Hard: {data.get('hard_solved', 0)}")
                
            elif agent_name == 'codeforces':
                print(f"\n🏆 Codeforces Stats:")
                # Try nested data first, then root level
                data = output.get('data', output)
                print(f"  Handle: {data.get('handle', 'N/A')}")
                print(f"  Rating: {data.get('rating', 0)}")
                print(f"  Max Rating: {data.get('max_rating', 0)}")
                print(f"  Rank: {data.get('rank', 'Unrated')}")
                print(f"  Max Rank: {data.get('max_rank', 'Unrated')}")
                print(f"  Contests: {data.get('contests_participated', 0)}")
                print(f"  Problems Solved: {data.get('problems_solved', 'N/A')}")
            
            print(f"\n📋 Full Output:")
            print(json.dumps(output, indent=2))
        
        break

if __name__ == "__main__":
    app_id = int(sys.argv[1]) if len(sys.argv) > 1 else 31
    asyncio.run(check_competitive_results(app_id))
