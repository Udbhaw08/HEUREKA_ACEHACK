# Fair Hiring Network – Complete System Documentation

**Version:** 3.0 Final | **For:** Antigravity Agent Development

---

## 📋 Quick Navigation

- [Project Overview](#1-project-overview)
- [5 Core Agents](#2-agent-architecture)
- [LangGraph Workflow](#3-langgraph-orchestration)
- [Tech Stack](#4-tech-stack)
- [Critical Rules](#8-critical-reminders)

---

## 1. PROJECT OVERVIEW

### Core Identity
- **Name:** Fair Hiring Network – Future of Work
- **Tagline:** *Fair hiring starts with fair systems. We verify both.*
- **Summary:** We verify skills through multiple fair paths, audit bias continuously, explain every decision, and carry trust into offline hiring—without blockchain.

### The Problem We Solve
1. **Skills claimed, not verified** → ATS keyword stuffing works
2. **Hidden bias** → Gender, college, age discrimination invisible
3. **Black-box screening** → No rejection explanations
4. **Paper fraud** → Offline certificates forgeable

### Our Solution (5 Agents)
1. **Company Fairness Agent** → Verifies companies BEFORE hiring
2. **Skill Verification Agent** → GitHub + Tests + Optional Protocall
3. **Bias Detection Agent** → Audits other agents (meta-monitoring)
4. **Matching Agent** → Transparent, explainable scoring
5. **Passport Agent** → Credentials without blockchain

---

## 2. AGENT ARCHITECTURE

### AGENT 1: Company Fairness Verification

**Input:** Job description  
**Output:** Fairness score (0-100)

**Checks:**
- Gendered language ("rockstar", "ninja")
- Age bias ("young team")
- College requirements
- Experience inflation

**LLM:** Claude Sonnet 4.5 ($3/1M tokens)  
**Critical Rule:** Only `score >= 60` enters pipeline

**Code Skeleton:**
```python
def verify_company(jd: str) -> dict:
    flags = scan_keywords(jd)
    llm_check = llm.invoke(f"Analyze bias: {jd}")
    score = 100 - (len(flags) * 10)
    return {"score": score, "status": "Approved" if score >= 60 else "Rejected"}
```

---

### AGENT 2: Multi-Stage Skill Verification

**3 Stages:**

**Stage 0: Anonymization**
- Strip: name, gender, college, age
- Create: `anonymous_id`

**Stage 1: GitHub Analysis**
- Check: commits, code quality, tech stack
- If strong (>70) → Skip test
- If weak → Trigger Stage 2

**Stage 2: Conditional Test**
- 15-25 min coding challenge
- Anti-cheating: explanation vs code match
- **Rule:** Test adjusts confidence, doesn't reject

**Stage 3: Protocall (Optional)**
- **Practice Mode (default):** No hiring impact
- **Hiring Signal Mode (opt-in):** 10% weight max
- Extracts: explanation clarity, concept understanding
- **Ignores:** accent, personality, appearance

**LLM:** Llama 3.1 8B ($0.06/1M)

**Final Output:**
```json
{
  "verified_skills": ["Python", "FastAPI"],
  "confidence": 86,
  "evidence": {"portfolio": 85, "test": 88, "protocall": 84}
}
```

---

### AGENT 3: Bias Detection (Meta-Agent)

**Purpose:** Audits OTHER agents for bias

**Monitors:**
1. **Gender** → Score gap >5 points
2. **College** → Tier-1 boost >10 points
3. **Protocall** → Accent discrimination >8 points

**LLM:** Llama 3.1 70B ($0.59/1M)

**Action:** Publishes `bias_alert`, triggers re-verification

**Code:**
```python
def detect_gender_bias(candidates):
    female_avg = mean([c['score'] for c in candidates if c['gender'] == 'F'])
    male_avg = mean([c['score'] for c in candidates if c['gender'] == 'M'])
    
    if male_avg - female_avg > 5:
        publish_redis("bias_alert", {"type": "gender", "gap": gap})
```

---

### AGENT 4: Transparent Matching

**Formula:**
```
score = (skill_confidence * 0.6) + 
        (experience * 0.3) + 
        (optional_protocall * 0.1)
```

**Excludes:** Gender, name, college, age, location

**Output (same for both parties):**
```json
{
  "score": 87,
  "breakdown": {"skills": 51.6, "experience": 25.5, "interview": 8.4},
  "matched": ["Python", "React"],
  "missing": [],
  "bias_check": "PASSED"
}
```

**LLM:** Gemini Pro 1.5 ($0.125/1M)

---

### AGENT 5: Skill Passport

**Security (No Blockchain):**
- Digital signature (RSA-2048)
- SHA-256 hash storage
- PostgreSQL registry

**NFC Offline:**
- Card contains: `credential_id` only
- Tap → Fetch → Verify → Display skills

**LLM:** Llama 3.1 8B ($0.06/1M)

---

## 3. LANGGRAPH ORCHESTRATION

### Workflow
```
START → verify_company (if score >= 60) → 
anonymize → portfolio_analysis (if weak) → 
test (optional) → protocall (optional) → 
aggregate → bias_detection (if no bias) → 
matching → passport → END
```

### State Schema
```python
class HiringState(TypedDict):
    company_fairness_score: int
    candidate_id: str  # anonymous
    portfolio_result: dict
    skill_credential: dict
    bias_report: dict
    match_scorecard: dict
```

### Implementation
```python
from langgraph.graph import StateGraph

graph = StateGraph(HiringState)
graph.add_node("verify_company", company_node)
graph.add_node("detect_bias", bias_node)
# ... add all 9 nodes

graph.add_conditional_edges(
    "verify_company",
    lambda s: "continue" if s["company_fairness_score"] >= 60 else "reject"
)

app = graph.compile()
```

---

## 4. TECH STACK

| Component | Technology | Cost |
|-----------|-----------|------|
| **Agent Framework** | LangGraph | Free |
| **Communication** | Redis Pub/Sub | Free (local) |
| **LLMs** | OpenRouter | $3.60/hackathon |
| **Protocall** | Gemini 2.5/2.0 Flash | Free tier |
| **Backend** | FastAPI + Python 3.11 | Free |
| **Database** | PostgreSQL 15 | Free (local) |
| **Frontend** | React 19 + TypeScript | Free |
| **Security** | RSA-2048 + SHA-256 | Free |

---

## 5. DESIGN PRINCIPLES

1. **Candidate-First** → Design for fairness, companies benefit secondarily
2. **Zero Agent Trust** → Bias agent monitors all others
3. **Explainability** → No black boxes, transparent scorecards
4. **Privacy** → PII never reaches matching agent
5. **Multiple Paths** → GitHub OR tests OR Protocall

---

## 6. CRITICAL CONSTRAINTS

- ✅ No single agent makes final decisions
- ✅ ATS keyword ranking FORBIDDEN
- ✅ Bias findings must be logged
- ✅ Same scorecard for both parties
- ✅ Protocall opt-in, 10% weight max
- ✅ No blockchain (use signatures)

---

## 7. PURPOSELY DISCARDED

| Feature | Reason |
|---------|--------|
| Mandatory interviews | Penalizes introverts |
| Long exams (>30 min) | Time-intensive |
| ATS keyword ranking | Rewards manipulation |
| Blockchain | Expensive, slow |
| Webcam surveillance | Privacy invasion |
| Personality scoring | Biased, subjective |

---

## 8. CRITICAL REMINDERS

### For Development

1. **NEVER** allow matching agent to see gender, name, college
2. Bias agent does NOT auto-reject (triggers review)
3. Protocall MUST be opt-in with 10% max weight
4. Same scorecard for both parties (no hidden data)
5. Use digital signatures, NOT blockchain
6. Test adjusts confidence, doesn't reject
7. All Redis events need timestamp + event_id
8. Use type hints for all functions
9. Cache LLM responses to save costs
10. NFC payload max 888 bytes

### Redis Event Channels
- `company_verified` → {company_id, score, status}
- `skill_verified` → {candidate_id, credential_id}
- `bias_alert` → {severity, report}  **CRITICAL**
- `match_completed` → {candidate_id, score, decision}
- `credential_issued` → {credential_id}

---

## 9. OUTPUT SCHEMAS

### Company Fairness Agent
```json
{
  "fairness_score": 82,
  "status": "Approved",
  "flags": [{"type": "gender", "keyword": "rockstar"}],
  "suggestions": ["Remove 'rockstar'"]
}
```

### Skill Verification Agent
```json
{
  "candidate_id": "anon_a7f3e9",
  "verified_skills": ["Python", "FastAPI"],
  "skill_confidence": 86,
  "evidence": {
    "portfolio_score": 85,
    "test_score": 88,
    "interview_signal": 84
  }
}
```

### Bias Detection Agent
```json
{
  "bias_detected": true,
  "checks": {
    "gender": {
      "bias_detected": true,
      "gap": 10.7,
      "recommendation": "Audit matching weights"
    }
  }
}
```

### Matching Agent
```json
{
  "overall_score": 87,
  "breakdown": {"skills": 51.6, "experience": 25.5},
  "matched_skills": ["Python", "React"],
  "bias_check": "PASSED"
}
```

---

## 10. SUCCESS CRITERIA

### Demo Targets
- Company fairness: 90%+ accuracy
- ATS detection: 85%+ catch rate
- Bias sensitivity: >5 point gaps detected
- Verification speed: <100ms
- Budget: <$4 total spend

---

## 11. IMPLEMENTATION ORDER

1. Setup: LangGraph + Redis + PostgreSQL + OpenRouter
2. Agent 1: Company Fairness
3. Agent 2: Skill Verification (3 stages)
4. Agent 3: Bias Detection
5. Agent 4: Matching
6. Agent 5: Passport
7. Integration: LangGraph workflow
8. Testing: Unit + Integration tests

---

## 12. COST OPTIMIZATION

- **Cache LLM responses** (SQLiteCache)
- **Compress prompts** (extract fields, not full text)
- **Progressive quality** (cheap first, expensive if needed)
- **Batch processing** (5 candidates in 1 call)

**Estimated Total:** $3.60 (from $10 budget)

---

## END OF DOCUMENTATION

**For Antigravity Development:**
- Use this as complete system context
- Ask agent: "Build Agent X following this spec"
- All design decisions are locked
- All schemas are final
- All constraints are mandatory

**Questions?** Refer to specific agent sections above.
```

---

### Step 4: Create Gist

1. Paste the markdown above
2. Set visibility: **Public** or **Secret** (your choice)
3. Click **"Create public gist"** or **"Create secret gist"**

### Step 5: Get The Link

GitHub will give you a URL like:
```
https://gist.github.com/yourusername/abc123def456
Step 6: Use in Antigravity