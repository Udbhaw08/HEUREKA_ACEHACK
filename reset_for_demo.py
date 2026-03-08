import os
import shutil
import sqlite3
from pathlib import Path

def reset():
    print("🚀 Resetting System for Professional Demo...")
    
    # 1. Clear Backend Data
    dirs_to_clear = [
        "backend/data/resumes",
        "backend/data/linkedin",
        "backend/data/jobs",
        "agents_files/uploads",
        "agents_files/processed"
    ]
    
    for d in dirs_to_clear:
        path = Path(d)
        if path.exists():
            print(f"  Cleaning {d}...")
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
        
    # 2. Reset Database (Comprehensive)
    db_path = "backend/fair_hiring.db"
    if os.path.exists(db_path):
        print("  Wiping SQLite database...")
        os.remove(db_path)
    
    # 3. Clear Logs
    log_files = [f for f in os.listdir(".") if f.endswith(".log") or (f.startswith("backend_log") and f.endswith(".txt"))]
    for log in log_files:
        print(f"  Removing {log}...")
        os.remove(log)

    # 4. Clear Agent State (Comprehensive)
    # Search root and backend
    search_paths = [".", "backend"]
    for base in search_paths:
        base_path = Path(base)
        if not base_path.exists(): continue
        for d in os.listdir(base):
            if d.startswith(".agent-"):
                agent_dir = base_path / d
                print(f"  Cleaning agent state {agent_dir}...")
                shutil.rmtree(agent_dir, ignore_errors=True)

    print("\n✅ System Reset Complete. Ready for a fresh start!")

if __name__ == "__main__":
    reset()
