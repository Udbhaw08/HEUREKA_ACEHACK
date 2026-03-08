"""
Check GitHub extraction results from database
"""
import asyncio
import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from sqlalchemy import text

async def check_github_results(application_id: int):
    """Check what GitHub agent extracted for an application"""
    
    async for db in get_db():
        # Get GitHub agent run
        query = text("""
            SELECT 
                agent_name,
                status,
                output_payload,
                created_at
            FROM agent_runs 
            WHERE application_id = :app_id 
            AND agent_name = 'github'
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        
        result = await db.execute(query, {"app_id": application_id})
        row = result.fetchone()
        
        if not row:
            print(f"❌ No GitHub results found for application {application_id}")
            return
        
        print("=" * 70)
        print(f"GITHUB RESULTS FOR APPLICATION {application_id}")
        print("=" * 70)
        
        print(f"\n📊 Status: {row[1]}")
        print(f"⏰ Processed: {row[3]}")
        
        output = row[2]
        
        print("\n🔍 GitHub Analysis:")
        print(f"  Success: {output.get('success')}")
        print(f"  GitHub Status: {output.get('data', {}).get('github_status')}")
        
        data = output.get('data', {})
        
        # Profile info
        profile = data.get('profile', {})
        if profile:
            print(f"\n👤 Profile:")
            print(f"  Username: {profile.get('username')}")
            print(f"  Name: {profile.get('name')}")
            print(f"  Bio: {profile.get('bio', 'N/A')[:100]}")
            print(f"  Public Repos: {profile.get('public_repos')}")
            print(f"  Followers: {profile.get('followers')}")
            print(f"  Account Age (years): {profile.get('account_age_years')}")
        
        # Skills detected
        skills = data.get('skills', {})
        if skills:
            print(f"\n🛠️ Skills Detected:")
            for category, skill_list in skills.items():
                if skill_list:
                    print(f"  {category}: {', '.join(skill_list[:10])}")
        
        # Repositories
        repos = data.get('repositories', [])
        if repos:
            print(f"\n📦 Repositories ({len(repos)} total):")
            for repo in repos[:5]:
                print(f"  - {repo.get('name')} ({repo.get('language', 'N/A')}) - ⭐ {repo.get('stars', 0)}")
        
        # Activity metrics
        metrics = data.get('activity_metrics', {})
        if metrics:
            print(f"\n📈 Activity Metrics:")
            print(f"  Total Commits: {metrics.get('total_commits')}")
            print(f"  Total Stars: {metrics.get('total_stars')}")
            print(f"  Active Days: {metrics.get('active_days')}")
        
        # Full output (optional)
        print(f"\n📋 Full Output (JSON):")
        print(json.dumps(output, indent=2))
        
        break

if __name__ == "__main__":
    app_id = int(sys.argv[1]) if len(sys.argv) > 1 else 29
    asyncio.run(check_github_results(app_id))
