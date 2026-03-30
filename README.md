# 🧠 Requirement Intelligence Agent

An AI-powered system designed to analyze unstructured software requirement documents (text or PDFs) and automatically translate them into structured **Functional/Non-Functional Requirements**, **Risk Analysis**, and actionable **Task Plans** using **Generative AI** (LLaMA 3.1 via Groq).

This project simulates how real-world product, engineering, and consulting teams decompose client prompts before kicking off development.

You can try this app here https://requirement-ai-system.vercel.app/

---

## 🚀 Features

The system accepts **Plain Text** or **PDF Uploads** and automatically generates:

- ✅ **Structured Requirements** (Functional & Non-Functional with source traceability)
- ⚠️ **Risk & Ambiguity Analysis** (Technical, scope, and operational risks + mitigation strategies)
- 🧩 **Task Breakdown** (Agile format: Epics → User Stories → Engineering Tasks with priority/effort estimation)
- 📊 **Excel Export** (Download complete analysis directly to `.xlsx`)
- 🔗 **Jira Integration** (Push Epics, Stories, and Tasks directly to your Atlassian board)

All outputs are powered by **LLaMA 3.1 8B** and served via a lightning-fast **FastAPI backend** with a beautiful, responsive UI.

---

## 🛠️ Quick Start Guide

### Prerequisites
- **Python 3.9+**
- A **Groq API Key** (Get one for free at [console.groq.com](https://console.groq.com))

### 1️⃣ Clone the Repository & Setup Environment
```bash
git clone https://github.com/Revuubot/Requirement-AI-system.git
cd Requirement-AI-system

# Create and activate a virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
Create a file named `.env` in the root directory and add your Groq API key:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 4️⃣ Run the Application
Start the FastAPI server using Uvicorn:
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 5️⃣ Open the App
Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🏗️ Architecture Overview

The system is built on an asynchronous, multi-stage LLM pipeline to ensure structured and reliable outputs.

```text
User Input (Text / PDF)
        ↓
   FastAPI Backend
        ↓
┌───────────────────────────────┐
│ Requirement Extractor (LLM)   │
│ Risk Analyzer (LLM)           │
│ Task Planner (LLM)            │
└───────────────────────────────┘
        ↓
 Structured JSON Output
        ↓
 UI / Excel Export / Jira Sync
 ```

### Tech Stack
- **Backend:** Python, FastAPI, Uvicorn
- **AI / LLM:** Groq SDK, LLaMA-3.1-8b-instant
- **Frontend:** HTML, CSS (Custom Design System), Vanilla JS
- **Data Processing:** pandas, openpyxl, PyMuPDF
- **Integrations:** Jira REST API

---

## 🔁 End-to-End Workflow

1. **Input Ingestion:** Users submit text or securely upload PDFs (parsed locally via PyMuPDF without OCR overhead).
2. **Requirement Extraction (LLM):** The model extracts functional/non-functional requirements and ties them directly to the source quotes.
3. **Risk Intelligence (LLM):** Identifies technical risks, ambiguities, and missing constraints in the original document.
4. **Task Decomposition (LLM):** Synthesizes requirements into Epics, Stories, and concrete engineering Tasks formatted for Agile teams.
5. **Output Delivery:** Results are displayed in the UI, and can be exported as Excel reports or automatically provisioned into Jira via the API.

---

## 🌍 Why This Matters

In real-world software development, unclear or incomplete requirements are a major cause of project delays, scope creep, and cost overruns. 

This project demonstrates how **Generative AI** can augment business analysts and engineering teams by:
- Identifying missing constraints before code is written
- Structuring vague ideas into immediate, actionable engineering tasks
- Eliminating manual copy-pasting via direct Jira and Excel pipelines

---

## ⚠️ Limitations & Assumptions
- Output quality heavily depends on the clarity of the input document.
- Highly domain-specific jargon may require prompt adjustments.
- Processing latency is dependent on the Groq API (though typically under 5 seconds).

---

## 📌 Future Improvements
- [ ] Retrieval-Augmented Generation (RAG) for large multi-document PRDs
- [ ] Streaming AI responses to the frontend for better UX
- [ ] Multi-document comparison and cross-reference conflict detection
- [ ] Add GitHub Issues sync via the GitHub API
