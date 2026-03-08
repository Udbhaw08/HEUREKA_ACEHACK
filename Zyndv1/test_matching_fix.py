
import sys
import os
from pathlib import Path

# Add paths for imports
CLEAN_SYS = Path("agents_files/Clean_Hiring_System")
if str(CLEAN_SYS) not in sys.path:
    sys.path.insert(0, str(CLEAN_SYS))
SKILL_DIR = CLEAN_SYS / "skill_verification_agent"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from matching_agent.agents.matching_agent import MatchingAgent

def test():
    agent = MatchingAgent()
    
    # Payload from user logs
    payload = {
        "credential": {
            "identity": {
                "name": "Udbhaw Anand",
                "public_links": ["linkedin_present", "github_present"],
                "candidate_id": 5,
                "application_id": 4
            },
            "skills": [
                {"skill": {"name": "Python", "score": 70}, "tier": "core"},
                {"skill": {"name": "JavaScript", "score": 70}, "tier": "core"},
                {"skill": {"name": "TypeScript", "score": 45}, "tier": "core"},
                {"skill": {"name": "PX4", "score": 70}, "tier": "core"},
                {"skill": {"name": "MAVSDK", "score": 70}, "tier": "core"},
                {"skill": {"name": "Computer Vision", "score": 45}, "tier": "core"},
                {"skill": {"name": "YOLOv8", "score": 25}, "tier": "core"},
                {"skill": {"name": "Object Detection", "score": 36}, "tier": "core"}
            ],
            "verified_skills": {
                "core": [{"name": "Python", "score": 70}],
                "frameworks": [{"name": "YOLO", "score": 45}],
                "infrastructure": [{"name": "Linux", "score": 25}],
                "tools": []
            },
            "experience": [
                {
                    "company": "Archanion Engineering",
                    "role": "Computer Vision & UAV Autonomy Engineer",
                    "timeframe": "Nov 2025 - Present",
                    "claims": [
                        {
                            "action": "Developing autonomous flight",
                            "technology": ["MAVSDK", "YOLO", "PX4"],
                            "evidence_strength": "medium"
                        }
                    ]
                }
            ],
            "github_score": 0.7,
            "cp_activity": False,
            "learning_velocity": 0.5
        },
        "job_description": {
            "title": "python enig",
            "role": "Python Developer",
            "strict_requirements": ["Python", "Pandas", "NumPy"],
            "matching_philosophy": {"learning_velocity_weight": 0.2},
            "problem_solving": {"required": False}
        }
    }
    
    jd = payload["job_description"]
    candidate = payload["credential"]
    
    print(f"Running match for JD: {jd['title']} and Candidate: {candidate['identity']['name']}")
    result = agent.match(jd, candidate)
    
    print("\nMATCH RESULT:")
    print(f"Match Score: {result['match_score']}%")
    print(f"Match Status: {result['match_status']}")
    print(f"Breakdown: {result['breakdown']}")
    print(f"Matched Skills: {result['analysis']['matched_skills']}")
    print(f"Missing Skills: {result['analysis']['missing_skills']}")

if __name__ == "__main__":
    test()
