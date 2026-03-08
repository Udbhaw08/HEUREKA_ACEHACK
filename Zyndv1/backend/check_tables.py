"""
Simple database verification script
"""
import asyncio
from sqlalchemy import text
from app.database import engine

async def check_database():
    print("Checking database tables...")
    print("=" * 50)
    
    async with engine.begin() as conn:
        # Get all tables
        result = await conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        
        tables = [row[0] for row in result]
        
        if tables:
            print(f"\n✓ Found {len(tables)} tables in database:\n")
            for table in tables:
                # Get row count
                count_result = await conn.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
                count = count_result.scalar()
                print(f"  ✓ {table:20s} ({count} rows)")
        else:
            print("\n✗ No tables found in database!")
            return False
    
    print("\n" + "=" * 50)
    print("✓ Database verification complete!")
    return True

if __name__ == "__main__":
    success = asyncio.run(check_database())
    exit(0 if success else 1)
