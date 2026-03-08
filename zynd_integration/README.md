# FairHiring × Zynd Integration (AICKATHON)

This folder turns your existing FairHiring “agent microservices” into a **Zynd agent network**:
- Each agent runs as a **Zynd webhook agent** (`/webhook`, `/webhook/sync`, `/health`)
- Agents are **discoverable** via Zynd Registry (capability search)
- Backend orchestration can switch to Zynd transport via `USE_ZYND=1`

> Note: This repo does **not** include any proprietary Zynd secrets or credentials.  
> You must supply your **ZYND_API_KEY** from the dashboard.

## 1) Install

From repo root:

```bash
pip install -r zynd_integration/requirements.txt
```

(Backend also gets `zyndai-agent==0.1.0` added in `backend/requirements.txt`.)

## 2) Configure env

Copy `Global_Env_Example.env` to `.env` (repo root) and set:

- `ZYND_API_KEY=...`
- (optional) change ports if needed

## 3) Start Zynd agents (local)

Run each agent in its own terminal:

```bash
python -m zynd_integration.agents.matching_agent
python -m zynd_integration.agents.bias_agent
python -m zynd_integration.agents.skill_agent
python -m zynd_integration.agents.ats_agent
python -m zynd_integration.agents.passport_agent
```

Each one prints:
- Agent ID
- Webhook URL (registered / visible)
- Capability metadata

## 4) Switch backend pipeline to Zynd

Set:

```env
USE_ZYND=1
```

Start backend as usual.

Backend `AgentClient.call_agent(...)` will:
1. discover target agent via `search_agents_by_capabilities(...)`
2. call its `/webhook/sync` endpoint
3. parse the JSON response and continue your pipeline

## 5) Capability mapping

Backend currently uses this capability mapping:
- matching → `["fair_hiring", "matching"]`
- bias → `["fair_hiring", "bias_detection"]`
- skill → `["fair_hiring", "skill_verification"]`
- ats → `["fair_hiring", "ats"]`
- passport → `["fair_hiring", "passport"]`

You can tune these in: `backend/app/agent_client.py`.

## What’s still “optional / next”
- Wrap data-source scrapers (GitHub/LeetCode/Codeforces/LinkedIn) as Zynd agents too.
- Add identity verification checks (`verify_agent_identity`) before trusting responses.
- Enable x402 monetization by setting `price` + `pay_to_address` in AgentConfig.
