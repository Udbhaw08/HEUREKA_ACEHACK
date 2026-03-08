import asyncio
import json
from app.agents.job_extraction import JobExtractionAgent

async def run_standalone_extraction():
    jd_text = """
Role: Software Engineer – Full-Stack & Systems (Early–Mid Level)

We are looking for a hands-on Software Engineer who has experience building, shipping, and iterating on real systems. This role values demonstrated ability, engineering judgment, and learning velocity over job titles or years of experience.

You will work across frontend, backend, and system components, contributing to products that handle real users, data, and scale.

Core Technical Requirements
Candidates must demonstrate practical experience in the following areas through projects, repositories, or deployed systems:

Programming Languages
JavaScript / TypeScript (production or large project usage)
Python (backend services, scripting, or automation)
At least one additional language (Go, Java, Rust, or C++)

Web Fundamentals
HTML, CSS
RESTful APIs
HTTP lifecycle and client–server interaction

Backend Engineering
Experience building backend services using Node.js, FastAPI, Django, or similar frameworks
Understanding of authentication, authorization, and basic security practices
Working knowledge of relational databases (PostgreSQL / MySQL)

Frontend & Framework Experience (Preferred)
Modern frontend frameworks:
React (preferred)
Vue or Angular (acceptable)
State management and component-based architecture
Ability to translate product requirements into usable interfaces

Systems, Data & Infrastructure (Supporting Skills)
Basic system design concepts:
API design
Data modeling
Scalability tradeoffs
Experience with at least one of:
Docker
Cloud platforms (AWS / GCP / Azure)
Message queues or background workers

Engineering Signals We Evaluate
We strongly value evidence over claims. We evaluate:
Ownership of GitHub projects (solo or primary contributor)
Code quality, structure, and readability
Commit history showing iteration and learning progression
Use of issues, documentation, and version control best practices
Problem-solving ability demonstrated via coding platforms such as:
LeetCode
Codeforces
AtCoder

What Is Not Required
Formal job titles or corporate experience
Specific company backgrounds
College pedigree or degrees
Perfect system design or large-scale production systems

Evaluation Philosophy
Partial skill matches are acceptable
Strong fundamentals with learning momentum are preferred over narrow specialization
Final matching is based on verified technical evidence, not resumes or self-reported proficiency
"""
    
    agent = JobExtractionAgent()
    print("--- STARTING JD INTELLIGENCE EXTRACTION (CLAUDE 3.5) ---")
    result = agent.extract(jd_text, title="Software Engineer – Full-Stack & Systems")
    
    print("\n--- STRUCTURED OUTPUT ---")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(run_standalone_extraction())
