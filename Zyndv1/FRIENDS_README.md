# 🚀 Fair Hiring Network: Technical Setup Guide

Follow these steps to get the environment ready for the demo.

## 🛠️ Step 1: Install Dependencies

### **Backend (Python)**
Ensure you have Python 3.12+ installed, then run:
```powershell
pip install -r backend/requirements.txt
```

### **Frontend (Node.js)**
Install the React dependencies:
```powershell
cd fair-hiring-frontend
npm install
cd ..
```

## ⚡ Step 2: External Tools (Optional)
If you want to run the **Bias Agent** locally using Llama 3.2:
1. Install [Ollama](https://ollama.com).
2. Run `ollama pull llama3.2`.

## ⚡ Step 3: Launching the System

### **1. The Agent Network & Backend**
We use a special script to launch everything in separate visible windows so you can see the AI agents working in real-time.
```powershell
.\start_demo.ps1
```

### **2. The Frontend UI**
In a separate terminal window:
```powershell
cd fair-hiring-frontend
npm run dev
```

## 🧪 How to Demo
1. Open `http://localhost:5173` in your browser.
2. **Employer Side**: Create a new Job Posting.
3. **Candidate Side**: Apply for that job using a resume and a GitHub link.
4. **The "Wow" Moment**: Switch back to your terminal windows. You will see the **ATS Agent**, **Skill Agent**, and **Bias Agent** communicating via the **Zynd Protocol** to verify the candidate and sign their Skill Passport!

---
*Since you already have the `.env` file, no further configuration is needed!*
