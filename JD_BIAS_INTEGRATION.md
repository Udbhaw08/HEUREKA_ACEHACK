# JD Bias Agent Integration Guide

This guide details how to integrate the `jd_bias_agent.py` into the Fair Hiring project. Follow these steps to replicate the integration.

## 📂 File Structure Overview

Ensure you are working within the main project directory (e.g., `Agents-main`).

```text
Agents-main/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   └── jd_bias.py       <-- [NEW FILE]
│   │   ├── routers/
│   │   │   └── agent.py         <-- [NEW FILE]
│   │   └── main.py              <-- [MODIFIED]
│   └── requirements.txt         <-- [MODIFIED]
└── fair-hiring-frontend/
    └── src/
        ├── api/
        │   └── backend.js       <-- [MODIFIED]
        └── components/
            └── CompanyHiringFlow.jsx <-- [MODIFIED]
```

---

## 🛠️ Backend Integration

### 1. Create the Agent Logic
**Location:** `backend/app/agents/jd_bias.py`
**Action:** Create this new file.
**Content:** This file contains the `JobBiasAgent` class that interacts with LangChain/Ollama.
- Ensure the folder `backend/app/agents/` exists. If not, create it.
- Copy the provided `JobBiasAgent` class code here. It handles the LLM prompt and JSON parsing.

### 2. Create the API Router
**Location:** `backend/app/routers/agent.py`
**Action:** Create this new file.
**Content:** This file defines the API endpoint.
- Define a `POST` endpoint at `/company/analyze_bias`.
- It receives `{ description: string }` and returns the agent's analysis.

### 3. Register the Router
**Location:** `backend/app/main.py`
**Action:** Modify existing file.
**Instructions:**
- Open `backend/app/main.py`.
- Find where other routers (like `company_router` or `auth_router`) are included.
- Add these lines:
  ```python
  from app.routers.agent import router as agent_router
  app.include_router(agent_router)
  ```

### 4. Update Dependencies
**Location:** `backend/requirements.txt`
**Action:** Modify existing file.
**Instructions:**
- Add the following lines to ensure the environment has necessary packages:
  ```text
  langchain_ollama
  PyPDF2
  cryptography
  ```

---

## 💻 Frontend Integration

### 1. Update API Client
**Location:** `fair-hiring-frontend/src/api/backend.js`
**Action:** Modify existing file.
**Instructions:**
- Find the `api` object export.
- Add the `analyzeJobDescription` function:
  ```javascript
  // Agents
  analyzeJobDescription: (description) =>
    request("/company/analyze_bias", {
      method: "POST",
      body: JSON.stringify({ description }),
    }),
  ```

### 2. Update UI Component
**Location:** `fair-hiring-frontend/src/components/CompanyHiringFlow.jsx`
**Action:** Modify existing file.
**Instructions:**
- **Import:** Ensure `api` is imported from `../api/backend`.
- **State:** Add `isAnalyzing` and `biasResult` states inside the component.
- **Logic:** Add `handleAnalyzeBias` function to call the API.
- **Render:** In the Job Description `<section>`, add the "RUN BIAS AUDIT" button and a container to display `biasResult` (score, reasoning, findings).

---

## ✅ Verification Steps

1.  **Start Backend:**
    ```bash
    cd backend
    pip install -r requirements.txt
    python -m uvicorn app.main:app --reload --port 8000
    ```
2.  **Start Frontend:**
    ```bash
    cd fair-hiring-frontend
    npm run dev
    ```
3.  **Test:**
    - Navigate to "Create New Role" in the UI.
    - Type a description (e.g., "Looking for a rockstar").
    - Click **RUN BIAS AUDIT**.
    - Verify the bias score appears red/green with findings.
