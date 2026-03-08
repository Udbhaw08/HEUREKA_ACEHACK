import asyncio
import sys
import os
import shutil
from pathlib import Path

# Add project roots to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "backend"))

async def wipe_database_and_files():
    """
    Consolidated script to wipe PostgreSQL data and temporary demo files.
    Use this to reset candidate details and start fresh.
    """
    print("🚀 Consolidating Wipe Process...")

    # 1. Clear PostgreSQL Database
    print("🔍 Connecting to PostgreSQL to reset data...")
    try:
        from backend.app.database import engine, init_db # type: ignore
        from backend.app.models import Base # type: ignore
        
        async with engine.begin() as conn:
            print("🗑️  Dropping all existing database tables...")
            await conn.run_sync(Base.metadata.drop_all)
            
        print("🏗️  Recreating schema...")
        await init_db()
        print("✅ Database reset successfully!")
    except Exception as e:
        print(f"⚠️  Database reset skipped or failed: {e}")

    # 2. Clear File System Data
    dirs_to_clear = [
        "backend/data/resumes",
        "backend/data/linkedin",
        "backend/data/jobs",
        "agents_files/uploads",
        "agents_files/processed"
    ]
    
    for d in dirs_to_clear:
        path = PROJECT_ROOT / d
        if path.exists():
            print(f"📁 Cleaning {d}...")
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)

    # 3. Clear Agent State
    search_paths = [PROJECT_ROOT, PROJECT_ROOT / "backend"]
    for base_path in search_paths:
        if not base_path.exists(): continue
        for item in base_path.iterdir():
            if item.is_dir() and item.name.startswith(".agent-"):
                print(f"🧹 Removing agent state: {item.name}")
                shutil.rmtree(item, ignore_errors=True)

    # 4. Clear Logs
    for log_file in PROJECT_ROOT.glob("*.log"):
        print(f"📄 Removing log: {log_file.name}")
        log_file.unlink()
    
    for log_file in PROJECT_ROOT.glob("backend_log*.txt"):
        print(f"📄 Removing log: {log_file.name}")
        log_file.unlink()

    print("\n✨ System is now 100% clean. You can reuse candidate details now!")

if __name__ == "__main__":
    asyncio.run(wipe_database_and_files())
