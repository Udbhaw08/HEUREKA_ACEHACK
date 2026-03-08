"""
Reset and recreate database tables
"""
import asyncio
from sqlalchemy import text
from app.database import engine

async def reset_database():
    print("Resetting database...")
    print("=" * 50)
    
    async with engine.begin() as conn:
        # Drop all ENUM types
        print("\n1. Dropping existing ENUM types...")
        enum_types = ['applicationstatus', 'pipelinestatus', 'agentrunstatus', 'reviewseverity', 'reviewstatus']
        for enum_type in enum_types:
            try:
                await conn.execute(text(f"DROP TYPE IF EXISTS {enum_type} CASCADE"))
                print(f"   ✓ Dropped {enum_type}")
            except Exception as e:
                print(f"   - {enum_type} (doesn't exist)")
        
        # Drop alembic version to reset migrations
        print("\n2. Resetting migration history...")
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))
        print("   ✓ Reset migration history")
    
    print("\n" + "=" * 50)
    print("✓ Database reset complete!")
    print("\nNow run: alembic upgrade head")

if __name__ == "__main__":
    asyncio.run(reset_database())
