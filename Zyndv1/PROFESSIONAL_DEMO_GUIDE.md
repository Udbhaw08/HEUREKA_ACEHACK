# 🏆 Professional Demo & Hackathon Winner's Guide

This guide ensures your recording is world-class, professional, and clearly demonstrates why **Zynd** is the beating heart of this system.

---

## 🎬 1. Preparation (The "Stage")

1.  **Launcher**: Use `.\ULTIMATE_DEMO_LAUNCHER.ps1`. It wipes the slate clean and tiles your terminal windows.
2.  **Layout**: Arrange the windows in a grid:
    *   **Top Row**: Backend (Main Engine) | Matching Agent | Bias Agent.
    *   **Bottom Row**: Passport Agent (Crucial!) | ATS Agent | Skill Agent.
3.  **Frontend**: Open `http://localhost:5173` in a clean browser window (F11 for full screen).
4.  **Code**: Have VS Code open on `backend/app/zynd_orchestrator.py` and `zynd_integration/agents/passport_agent.py`.

---

## 📽️ 2. The Multi-Act Script

### Act 1: The "Fair" Job Creation (Company Side)
*   **Narrative**: "Traditional job postings are filled with unconscious bias. We build trust from Step 1."
*   **Action**: Create a job (e.g., 'Senior Drone Engineer').
*   **Visual**: Switch back to the **Bias Agent** terminal. Show it analyzing the text in real-time.
*   **Technical High**: Point out how the agent is a registered Zynd identity, ensuring the audit itself can't be tampered with.

### Act 2: The Unified Skill Passport (Candidate Side)
*   **Narrative**: "Why re-verify every time? We create a Verifiable Credential (VC) that is cryptographically signed."
*   **Action**: Apply for the job. 
*   **Visual**: Switch to the **Passport Agent** terminal. You will see:
    ```
    [passport] Protocol: ZYND-SIGNATURE
    [passport] Credential issued for Candidate ANON-XXXX
    [passport] Signature created using Ed25519
    ```
*   **Technical High**: Explain that this signature is stored on the candidate's "Skill Passport," which they own.

### Act 3: The Multi-Agent Consensus (The Engine)
*   **Narrative**: "The Fair Hiring Network isn't one AI—it's a decentralized network of specialists."
*   **Action**: Watch the Backend logs. You will see `[zynd-orch]` discovery logs.
*   **Visual**: Show the **Matching** and **Skill** agents firing in parallel.
*   **Technical High**: "The Orchestrator discovers these agents on the Zynd Registry dynamically. We don't hardcode URLs; we discover capabilities."

### Act 4: The Proof (The Code)
*   **Action**: Briefly show `zynd_orchestrator.py`.
*   **Visual**: Highlight `orch.call_sync` and `orch.discover`.
*   **Technical High**: "We've moved beyond simple APIs to a Verifiable Agent Protocol."

---

## 💎 3. Winner's Tips

1.  **Speak with Confidence**: Don't say "I think it works," say "The system enforces trust through cryptography."
2.  **The "Wow" Moment**: When you show the **Skill Passport UI** (the card with the verify check), click "View Technical Signature." Show the JSON and the Signature string. "This is the proof that makes our hiring fair."
3.  **Mention the Hackathon**: "By leveraging Zynd, we solved the trust problem of AI agents in 48 hours."

---

## 🚀 4. Final Verification Checklist
- [ ] `ollama pull llama3.2` is done (for Bias Agent).
- [ ] `.env` has `USE_ZYND=1`.
- [ ] You have a sample resume PDF in a folder you can easily drag-and-drop.

**Go win that 1st Place! 🚀**
