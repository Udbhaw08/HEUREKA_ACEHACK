# 🚀 How We Used Google Antigravity to Build Fair Hiring Network

## Overview

**Google Antigravity** was our primary development environment throughout the ACEHACK hackathon. It served as the agentic backbone for building, debugging, and shipping the **Fair Hiring Network (FHN)** — a multi-agent AI-powered recruitment platform. Antigravity's context-aware agent, inline code commands, and tab autocompletion dramatically accelerated our development cycle across every layer of the stack.

---

## 🏗️ Architecture Built with Antigravity

```
┌──────────────────────────────────────────────────────────────────┐
│   FRONTEND (React + Vite)          Built with Antigravity        │
│   49 Components • Auth0 • Three.js • Glassmorphism UI            │
├──────────────────────────────────────────────────────────────────┤
│   BACKEND (FastAPI)                Debugged with Antigravity      │
│   8 API Routers • Async DB • Pipeline Orchestration              │
├──────────────────────────────────────────────────────────────────┤
│   ZYND AGENT MESH (9 Agents)       Integrated with Antigravity   │
│   ATS • Skill • Bias • Matching • Passport • GitHub • LinkedIn   │
├──────────────────────────────────────────────────────────────────┤
│   INFRA & DEVOPS                   Automated with Antigravity     │
│   PowerShell Scripts • Environment Config • Git Workflows        │
└──────────────────────────────────────────────────────────────────┘
```

---

## 1. 🎨 Frontend Development

### What We Built
A **premium, dark-themed React dashboard** with 49 components including:
- **Candidate Experience**: Signup, job browsing, application tracking, Skill Passport viewer
- **Company Dashboard**: Job posting, candidate pipeline visualization, bias reports
- **InterviewAI (Protocall)**: Real-time AI-powered interview sessions with ElevenLabs voice synthesis
- **Landing Page**: Three.js parallax effects, animated preloader, glassmorphism cards

### How Antigravity Helped
- **Component Generation**: Antigravity's agent scaffolded entire React components from natural language descriptions. For example, we described the Skill Passport UI as "a credential card with Ed25519 verification badges" and the agent generated the full `SkillPassport.jsx` component with proper API integration.
- **Styling Iteration**: We used inline code commands to rapidly iterate on CSS — adjusting gradients, animations, and responsive layouts without leaving the editor.
- **API Layer**: The agent auto-generated the `backend.js` API client with dynamic base URL detection, auth token management, and proper error handling for all 20+ endpoints.
- **Auth0 Integration**: Antigravity guided us through the complete Auth0 setup — generating the `useAuth.js` hook, configuring the Auth0 provider in `App.jsx`, and wiring up the `auth0-sync` backend endpoint.
- **Navbar & Preloader**: Built a "Stranger Things"-inspired preloader and scroll-aware navbar with appear/disappear behavior — all through iterative agent conversations.

---

## 2. ⚙️ Backend Development

### What We Built
A **FastAPI async backend** with:
- 8 API routers (Auth, Candidate, Company, Job, Application, Pipeline, Passport, Health)
- Async PostgreSQL with SQLAlchemy 2.0
- Ed25519 cryptographic signing for Skill Passports
- 10-stage pipeline orchestrator coordinating 9 AI agents
- JWT authentication with Auth0 verification

### How Antigravity Helped
- **Pipeline Orchestrator**: The most complex piece — a 10-stage pipeline (ATS → GitHub → LeetCode → Codeforces → LinkedIn → Skill → Bias → Matching → Passport). Antigravity's agent helped design the fault-tolerant orchestration flow in `agent_client.py`, including retry logic with exponential backoff.
- **Database Models**: We described our data model in plain English and the agent generated the complete SQLAlchemy async models (`models.py`) with proper relationships, indexes, and JSONB fields.
- **Zynd SDK Integration**: The agent helped build the `zynd_orchestrator.py` — a bridge between our backend and the Zynd agent mesh. It implemented DID-based agent discovery, webhook-based synchronous communication, and graceful fallback to direct HTTP when Zynd is unavailable.
- **Bug Fixing**: When the matching agent showed a persistent "16/100" score, Antigravity traced the issue to a normalization error in nested skill dictionaries and generated the schema adaptation code that correctly flattens tiered skill structures.
- **Resilient Architecture**: Antigravity refactored the Zynd import from eager (module-level) to lazy loading, ensuring the backend **always starts** regardless of whether the Zynd SDK or registry is available. This was critical for demo reliability.

---

## 3. 🤖 Zynd Agent Integration

### What We Built
9 specialized AI agents running as independent microservices, communicating via the Zynd protocol:

| Agent | Port | Purpose |
|-------|------|---------|
| ATS Guard | 5104 | Resume fraud detection & hidden text analysis |
| Skill Verifier | 5103 | Multi-source skill validation with LLM |
| Bias Detector | 5102 | Hiring discrimination pattern analysis |
| Matching Engine | 5101 | Semantic candidate-job matching |
| Passport Issuer | 5105 | Ed25519-signed credential generation |
| GitHub Parser | 5106 | Repository analysis & commit patterns |
| LinkedIn Parser | 5107 | Professional history extraction |
| Skill Test Agent | 5109 | AI-powered interview & test generation |
| Orchestrator | 5100 | DID-based agent discovery & routing |

### How Antigravity Helped
- **Agent Architecture**: Antigravity helped design the common agent base class (`zynd_integration/agents/common.py`) that all 9 agents extend, standardizing webhook handling, DID registration, and message processing.
- **Debugging Agent Communication**: When agents returned `401 Unauthorized` from the Zynd registry, Antigravity diagnosed that stale agent IDs (from a different user's environment) were being reused. It then updated the `reset_for_demo.py` script to comprehensively clear all `.agent-*` state directories.
- **Fallback Logic**: The agent implemented a dual-path communication system — Zynd webhook/sync for production and direct HTTP for local development — with automatic failover.

---

## 4. 🛠️ DevOps & Environment Management

### What We Built
- Unified startup scripts (`start_demo.ps1`, `start_all.ps1`) launching 9+ processes
- Environment-agnostic configuration with `$PSScriptRoot` resolution
- Automated port cleanup, process management, and log rotation
- Git workflow automation

### How Antigravity Helped
- **Cross-Machine Portability**: The project was originally developed on another machine (`D:\ZyndHiring\Zyndv1` by user `tabas`). When we cloned it to a new machine (`C:\Users\adars\Downloads\Zyndv1`), Antigravity identified and fixed **all hardcoded paths** across 5 PowerShell scripts and the Python virtual environment (`pyvenv.cfg`).
- **Startup Script Rewrite**: Antigravity rewrote `start_demo.ps1` to:
  - Auto-detect the venv Python executable
  - Set absolute `PYTHONPATH` for child processes
  - Run `reset_for_demo.py` before startup to clear stale state
  - Set correct working directories (backend needs `backend/` CWD, agents need project root)
- **Git Operations**: Antigravity managed remote URL changes and force-pushed to the hackathon repository when the original remote was no longer accessible.

---

## 5. 🔍 Debugging & Problem Solving

### Critical Issues Resolved with Antigravity

| Issue | Root Cause | Antigravity's Solution |
|-------|-----------|----------------------|
| `ModuleNotFoundError: No module named 'app'` | Missing `PYTHONPATH` and wrong CWD for uvicorn | Fixed all startup scripts with absolute paths and proper WorkingDirectory |
| `401 Unauthorized` from Zynd Registry | Stale agent IDs from different user/API key | Comprehensive reset script clearing all `.agent-*` directories |
| `ERR_CONNECTION_REFUSED` on frontend | Backend process dying silently | Made Zynd init lazy + fault-tolerant so backend always survives |
| `pyvenv.cfg` pointing to wrong Python | VirtualEnv created on different machine | Updated all paths in pyvenv.cfg to match current machine |
| Match score stuck at 16/100 | Normalization error in nested skill dicts | Schema adaptation code to flatten tiered structures |
| Pipeline crash on null ATS evidence | Missing null-safety in orchestrator | Added defensive `.get()` chains throughout pipeline |

---

## 6. 📊 Impact Summary

| Metric | Value |
|--------|-------|
| **Total Files Touched by Antigravity** | 40+ |
| **Frontend Components Generated/Refined** | 49 |
| **Backend Endpoints Built** | 20+ |
| **AI Agents Integrated** | 9 |
| **Critical Bugs Fixed** | 6 |
| **Scripts Automated** | 5 |
| **Lines of Code Across Stack** | ~15,000+ |
| **Time Saved (estimated)** | 60-70% vs manual development |

---

## 💡 What Made Antigravity Essential

1. **Context Awareness**: Antigravity understood our entire codebase — frontend, backend, agents, and infrastructure — simultaneously. It could trace a bug from a React component through the API layer to a specific agent's response format.

2. **Multi-File Editing**: Complex changes like the Zynd resilience refactor touched `agent_client.py`, `main.py`, `start_demo.ps1`, `start_all.ps1`, and `reset_for_demo.py` — all coordinated in a single conversation.

3. **Terminal Integration**: Running commands, checking port status, verifying health endpoints, and monitoring logs — all without leaving the editor.

4. **Iterative Refinement**: We could describe a UI change in natural language, see the code generated, test it in the browser, and iterate — all within minutes.

5. **Cross-Stack Debugging**: When the frontend showed `ERR_CONNECTION_REFUSED`, Antigravity traced it through the network layer → backend process → Zynd SDK crash → module-level import → stale config files, fixing the entire chain.

---

*Built with ❤️ using Google Antigravity at ACEHACK 2026*
*Team HEUREKA*
