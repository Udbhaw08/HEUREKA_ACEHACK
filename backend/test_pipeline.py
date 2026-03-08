"""
Test script for Fair Hiring System Backend

This script tests the complete pipeline:
1. Creates a test candidate
2. Submits a test application
3. Runs the full analysis pipeline
4. Verifies data persistence
5. Displays the generated credential
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
AGENT_SERVICES = {
    "ats": "http://localhost:8004",
    "github": "http://localhost:8005",
    "leetcode": "http://localhost:8006",
    "linkedin": "http://localhost:8007",
    "skill": "http://localhost:8003",
    "bias": "http://localhost:8002",
    "matching": "http://localhost:8001",
    "passport": "http://localhost:8008",
}


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message: str):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")


def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_header(message: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


async def check_backend_health() -> bool:
    """Check if backend is running"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print_success("Backend is running and healthy")
                return True
            else:
                print_error(f"Backend returned status {response.status_code}")
                return False
    except Exception as e:
        print_error(f"Cannot connect to backend: {e}")
        return False


async def check_agent_services() -> Dict[str, bool]:
    """Check if all agent services are running"""
    print_info("Checking agent services...")
    results = {}
    
    for service_name, service_url in AGENT_SERVICES.items():
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{service_url}/health")
                if response.status_code == 200:
                    print_success(f"{service_name.upper()} agent is running")
                    results[service_name] = True
                else:
                    print_warning(f"{service_name.upper()} agent returned status {response.status_code}")
                    results[service_name] = False
        except Exception as e:
            print_error(f"{service_name.upper()} agent is not reachable: {e}")
            results[service_name] = False
    
    return results


async def create_test_candidate() -> Dict[str, Any]:
    """Create a test candidate"""
    print_info("Creating test candidate...")
    
    candidate_data = {
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "name": "Test Candidate",
        "password": "test123",
        "gender": "prefer_not_to_say",
        "college": "Test University",
        "engineer_level": "mid"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{BASE_URL}/api/candidates/register",
                json=candidate_data
            )
            
            if response.status_code == 200:
                candidate = response.json()
                print_success(f"Created candidate: {candidate['anon_id']}")
                return candidate
            else:
                print_error(f"Failed to create candidate: {response.text}")
                return None
    except Exception as e:
        print_error(f"Error creating candidate: {e}")
        return None


async def create_test_job() -> Dict[str, Any]:
    """Create a test job"""
    print_info("Creating test job...")
    
    job_data = {
        "company_id": "COMP-TEST001",
        "title": "Senior Python Developer",
        "description": """
        We are looking for a Senior Python Developer with experience in:
        - Python 3.8+
        - FastAPI/Django
        - PostgreSQL
        - Docker
        - AWS/GCP
        - Strong problem-solving skills
        - Experience with AI/ML is a plus
        """,
        "max_participants": 10,
        "application_deadline": "2026-12-31T23:59:59"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{BASE_URL}/api/jobs",
                json=job_data
            )
            
            if response.status_code == 200:
                job = response.json()
                print_success(f"Created job: {job['id']} - {job['title']}")
                return job
            else:
                print_error(f"Failed to create job: {response.text}")
                return None
    except Exception as e:
        print_error(f"Error creating job: {e}")
        return None


async def submit_application(candidate_id: str, job_id: int) -> Dict[str, Any]:
    """Submit a test application"""
    print_info("Submitting application...")
    
    application_data = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "resume_text": """
        John Doe
        Senior Python Developer
        
        Experience:
        - 5 years of Python development
        - Built scalable web applications with FastAPI
        - Experience with PostgreSQL, Redis, Docker
        - Deployed applications on AWS
        
        Skills:
        - Python, JavaScript, TypeScript
        - FastAPI, Django, Flask
        - PostgreSQL, MongoDB
        - Docker, Kubernetes
        - AWS, GCP
        
        Education:
        - B.Tech Computer Science, Test University (2018)
        """,
        "github_url": "https://github.com/torvalds/linux",
        "leetcode_url": "https://leetcode.com/u/testuser/",
        "linkedin_url": "https://linkedin.com/in/testuser"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{BASE_URL}/api/applications",
                json=application_data
            )
            
            if response.status_code == 200:
                application = response.json()
                print_success(f"Submitted application: {application['id']}")
                return application
            else:
                print_error(f"Failed to submit application: {response.text}")
                return None
    except Exception as e:
        print_error(f"Error submitting application: {e}")
        return None


async def run_pipeline(application_id: int) -> Dict[str, Any]:
    """Run the full analysis pipeline"""
    print_info("Running analysis pipeline...")
    print_warning("This may take 1-2 minutes as it calls all agent services...")
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{BASE_URL}/api/pipeline/run",
                json={"application_id": application_id}
            )
            
            if response.status_code == 200:
                result = response.json()
                print_success(f"Pipeline completed successfully")
                print_info(f"Status: {result.get('status')}")
                return result
            else:
                print_error(f"Pipeline failed: {response.text}")
                return None
    except Exception as e:
        print_error(f"Error running pipeline: {e}")
        return None


async def verify_data_persistence(application_id: int) -> bool:
    """Verify that data was persisted to database"""
    print_info("Verifying data persistence...")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Get application details
            response = await client.get(f"{BASE_URL}/api/applications/{application_id}")
            
            if response.status_code == 200:
                application = response.json()
                print_success("Application data persisted")
                
                # Check if credential was created
                if application.get('credential_id'):
                    print_success(f"Credential created: {application['credential_id']}")
                    
                    # Get credential details
                    cred_response = await client.get(
                        f"{BASE_URL}/api/pipeline/result/{application_id}"
                    )
                    
                    if cred_response.status_code == 200:
                        credential = cred_response.json()
                        print_success("Credential data persisted")
                        
                        # Verify credential structure
                        if 'credential_json' in credential:
                            cred_json = credential['credential_json']
                            print_info(f"Verified skills: {len(cred_json.get('verified_skills', {}).get('core', []))}")
                            print_info(f"Skill confidence: {cred_json.get('skill_confidence', 0)}%")
                            return True
                
                return True
            else:
                print_error("Failed to retrieve application data")
                return False
    except Exception as e:
        print_error(f"Error verifying data persistence: {e}")
        return False


def display_credential_summary(credential: Dict[str, Any]):
    """Display a summary of the generated credential"""
    print_header("CREDENTIAL SUMMARY")
    
    cred_json = credential.get('credential_json', {})
    
    # Candidate info
    print(f"{Colors.BOLD}Candidate:{Colors.END}")
    print(f"  Name: {cred_json.get('candidate_name', 'N/A')}")
    print(f"  ID: {cred_json.get('candidate_id', 'N/A')}")
    print()
    
    # Overall score
    print(f"{Colors.BOLD}Overall Score:{Colors.END}")
    confidence = cred_json.get('skill_confidence', 0)
    color = Colors.GREEN if confidence >= 70 else Colors.YELLOW if confidence >= 50 else Colors.RED
    print(f"  {color}{confidence}% Confidence{Colors.END}")
    print()
    
    # Verified skills
    print(f"{Colors.BOLD}Verified Skills:{Colors.END}")
    verified_skills = cred_json.get('verified_skills', {})
    
    for category, skills in verified_skills.items():
        if skills:
            print(f"  {category.capitalize()}:")
            for skill in skills[:5]:  # Show first 5
                print(f"    • {skill}")
            if len(skills) > 5:
                print(f"    ... and {len(skills) - 5} more")
    print()
    
    # Evidence summary
    print(f"{Colors.BOLD}Evidence Sources:{Colors.END}")
    evidence = cred_json.get('evidence', {})
    
    for source, data in evidence.items():
        if data:
            print(f"  {source.capitalize()}: ✓")
        else:
            print(f"  {source.capitalize()}: ✗")
    print()
    
    # Match score
    if 'evidence' in evidence and 'matching' in evidence['matching']:
        match_data = evidence['matching']
        print(f"{Colors.BOLD}Match Score:{Colors.END}")
        print(f"  Overall: {match_data.get('overall_match_score', 0)}%")
        print(f"  Status: {match_data.get('match_status', 'N/A')}")
    print()


async def main():
    """Main test execution"""
    print_header("FAIR HIRING SYSTEM - BACKEND TEST")
    
    # Step 1: Check backend health
    print_header("STEP 1: Health Check")
    if not await check_backend_health():
        print_error("Backend is not running. Please start the backend server first.")
        print_info("Run: cd Agents-main/backend && python -m app.main")
        return
    
    # Step 2: Check agent services
    print_header("STEP 2: Agent Services Check")
    agent_status = await check_agent_services()
    
    # Check if critical agents are running
    critical_agents = ['ats', 'github', 'skill', 'matching', 'passport']
    missing_agents = [name for name in critical_agents if not agent_status.get(name)]
    
    if missing_agents:
        print_warning(f"Missing critical agents: {', '.join(missing_agents)}")
        print_info("Some tests may fail. Start missing agents with:")
        print_info("  cd Agents-main/agents_services && python start_all.py")
    else:
        print_success("All critical agents are running")
    
    # Step 3: Create test candidate
    print_header("STEP 3: Create Test Candidate")
    candidate = await create_test_candidate()
    if not candidate:
        print_error("Failed to create candidate. Aborting test.")
        return
    
    # Step 4: Create test job
    print_header("STEP 4: Create Test Job")
    job = await create_test_job()
    if not job:
        print_error("Failed to create job. Aborting test.")
        return
    
    # Step 5: Submit application
    print_header("STEP 5: Submit Application")
    application = await submit_application(candidate['id'], job['id'])
    if not application:
        print_error("Failed to submit application. Aborting test.")
        return
    
    # Step 6: Run pipeline
    print_header("STEP 6: Run Analysis Pipeline")
    pipeline_result = await run_pipeline(application['id'])
    if not pipeline_result:
        print_error("Pipeline execution failed. Aborting test.")
        return
    
    # Step 7: Verify data persistence
    print_header("STEP 7: Verify Data Persistence")
    if not await verify_data_persistence(application['id']):
        print_error("Data persistence verification failed.")
        return
    
    # Step 8: Display credential
    print_header("STEP 8: Display Credential")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/api/pipeline/result/{application['id']}")
            if response.status_code == 200:
                credential = response.json()
                display_credential_summary(credential)
                
                # Save full credential to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"test_credential_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(credential, f, indent=2)
                print_success(f"Full credential saved to: {filename}")
    except Exception as e:
        print_error(f"Error displaying credential: {e}")
    
    # Final summary
    print_header("TEST SUMMARY")
    print_success("All tests completed successfully!")
    print_info(f"Candidate ID: {candidate['anon_id']}")
    print_info(f"Application ID: {application['id']}")
    print_info(f"Job ID: {job['id']}")
    print()
    print_info("You can view the API documentation at:")
    print_info(f"  {BASE_URL}/docs")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_warning("\nTest interrupted by user")
    except Exception as e:
        print_error(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()