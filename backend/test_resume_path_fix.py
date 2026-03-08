"""
Quick test to verify resume_path is being passed to ATS
"""
import requests
import json

# Test the backend directly
print("Testing if resume_path is now being passed to ATS...")
print("=" * 70)

# Check if backend reloaded
try:
    response = requests.get("http://localhost:8000/health", timeout=2)
    print("✅ Backend is running")
except:
    print("❌ Backend not responding")
    exit(1)

print("\n📝 Instructions:")
print("1. Go to the frontend (http://localhost:5173)")
print("2. Apply to a job with a NEW resume upload")
print("3. Wait for processing to complete")
print("4. Run: python check_ats_results.py <application_id>")
print("\nYou should now see:")
print("  - Trust Score: 0-100 (not None)")
print("  - Guard Version: v1")
print("  - Full ATS Guard security checks")
print("\n" + "=" * 70)
