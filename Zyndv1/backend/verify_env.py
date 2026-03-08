import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Simulate main.py behavior
BASE_DIR = Path(__file__).resolve().parent.parent
print(f"Loading env from: {BASE_DIR / '.env'}")
load_dotenv(BASE_DIR / ".env")

# Add backend to sys.path
sys.path.append(str(Path(__file__).resolve().parent))

try:
    from app.config import settings
    print("✅ Configuration loaded successfully.")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"ATS_AGENT_URL: {settings.ATS_AGENT_URL}")
    print(f"PASSPORT_AGENT_URL: {settings.PASSPORT_AGENT_URL}")
    print(f"Services URL (Env var check): {os.getenv('ATS_SERVICE_URL')}")
    print(f"Signing Key Present: {bool(settings.SIGNING_PRIVATE_KEY_B64)}")
except Exception as e:
    print(f"❌ Configuration load failed: {e}")
