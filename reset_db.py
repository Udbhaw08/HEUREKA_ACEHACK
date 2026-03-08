import asyncio
import sys
import os
from pathlib import Path

# Add project roots to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "backend"))

async def reset_postgres():
    """
    Drops all tables and recreates them in PostgreSQL.
    """
    print("🔍 Connecting to PostgreSQL to reset data...")
    try:
        from backend.app.database import engine, init_db # type: ignore
        from backend.app.models import Base # type: ignore
        
        # Drop all tables synchronously within the async connection
        async with engine.begin() as conn:
            print("🗑️  Dropping all existing tables...")
            await conn.run_sync(Base.metadata.drop_all)
            
        # Recreate all tables
        print("🏗️  Recreating schema...")
        await init_db()
        
        print("✅ PostgreSQL reset successfully!")
    except Exception as e:
        print(f"❌ Failed to reset PostgreSQL: {e}")
        print("💡 Make sure your .env has the correct DATABASE_URL and Postgres is running.")

if __name__ == "__main__":
    asyncio.run(reset_postgres())
