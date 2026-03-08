import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def check():
    print(f"Checking connection to: {DATABASE_URL}")
    try:
        # Try to connect to postgres database first to check if the target db exists
        # or just try to connect to the target db directly.
        engine = create_async_engine(DATABASE_URL)
        async with engine.connect() as conn:
            print("Successfully connected to the database!")
            await conn.close()
        await engine.dispose()
        return True
    except Exception as e:
        print(f"Failed to connect: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(check())
