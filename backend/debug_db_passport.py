
import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.getcwd())

from app.database import init_db, get_db, AsyncSessionLocal
from app.models import Candidate, Credential
from sqlalchemy import select
from app.passport import verify_credential, get_public_key
from app.config import settings

async def debug_check():
    anon_id = "ANON-09CDD490CCD3"
    print(f"Checking for {anon_id}...")
    
    async with AsyncSessionLocal() as db:
        # Check Candidate
        q = await db.execute(select(Candidate).where(Candidate.anon_id == anon_id))
        cand = q.scalar_one_or_none()
        if not cand:
            print("❌ Candidate NOT FOUND in DB.")
            return

        print(f"✅ Found Candidate: {cand.id} ({cand.email})")

        # Check Credential
        q2 = await db.execute(select(Credential).where(Credential.candidate_id == cand.id).order_by(Credential.issued_at.desc()))
        cred = q2.scalars().first()
        
        if not cred:
            print("❌ No Credential found.")
            return

        print(f"✅ Found Credential ID: {cred.id}")
        
        # Check Key Mismatch
        import hashlib
        import base64
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        
        SEED = b"fair-hiring-network-seed-2026-xyz"
        derived_priv = Ed25519PrivateKey.from_private_bytes(hashlib.sha256(SEED).digest())
        derived_pub = derived_priv.public_key()
        
        derived_pub_b64 = base64.b64encode(derived_pub.public_bytes_raw()).decode()
        derived_priv_b64 = base64.b64encode(derived_priv.private_bytes_raw()).decode()
        
        env_pub_b64 = settings.SIGNING_PUBLIC_KEY_B64
        
        print(f"Agent Derived PubKey:  {derived_pub_b64}")
        print(f"Agent Derived PrivKey: {derived_priv_b64}")
        print(f"Backend Env PubKey:    {env_pub_b64}")
        
        # Check Payload Integrity
        from app.passport import canonical_json, sha256_hex
        
        stored_json = cred.credential_json
        calculated_hash = sha256_hex(canonical_json(stored_json))
        stored_hash = cred.hash_sha256
        
        print(f"Stored Hash:     {stored_hash}")
        print(f"Calculated Hash: {calculated_hash}")
        
        if stored_hash != calculated_hash:
            print("❌ HASH MISMATCH! The stored JSON is different from what was signed/hashed.")
        else:
            print("✅ Hash Integrity Valid")

        # Verify
        try:
            ok = verify_credential(cred.credential_json, cred.signature_b64)
            print(f"✅ Verification Result: {ok}")
        except Exception as e:
            print(f"❌ Verification Crashed: {e}")

if __name__ == "__main__":
    import uvicorn
    # run async
    asyncio.run(debug_check())
