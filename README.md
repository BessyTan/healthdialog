HealthDialog – Clinically-Grounded Health Triage Chatbot (FAISS + GPT-4 RAG)

A safe, explainable medical triage assistant powered by RAG, FAISS, SentenceTransformers, and GPT-4.
Provides grounded medical answers using real clinical data while estimating confidence and hallucination risk.

HealthDialog is not a medical device and not a substitute for emergency care.
If you are experiencing severe symptoms (chest pain, breathing difficulty, stroke signs), call emergency services.

Features
Retrieval-Augmented Generation (RAG)
    Vector search via FAISS
    Clinical question–answer dataset (clinical_faq.csv)
    Dynamically builds “clinical sources” context for GPT-4

GPT-4 Grounded Answer Generation
    GPT-4 synthesizes triage guidance grounded only in retrieved sources
    Strict rules: no diagnosis, no speculation, emergency escalation

Confidence + Hallucination Risk
    Confidence based on FAISS distance
    Risks: low, medium, high

Bullet-proof OpenAI API integration
    Key loaded via .env
    Passed explicitly to avoid uvicorn child-process issues
    Zero 500-errors (automatic fallback to FAQ answer)

Modern Frontend (Vite + React)
    Live chat interface
    Sources viewer
    Confidence + risk badges
    Simple and clean UI

Project Structure
healthdialog/
│
├── src/
│   ├── app.py                 # FastAPI API (CORS + /ask endpoint)
│   ├── rag_pipeline.py        # GPT-4 grounded RAG pipeline
│   ├── embed_store.py         # FAISS + SentenceTransformer embeddings
│   ├── data_loader.py         # CSV + JSON loaders
│   ├── config.py              # Loads OPENAI_API_KEY, GPT_MODEL
│   ├── hallucination_detector.py (optional)
│
├── data/
│   ├── clinical_faq.csv       # Clinical Q/A used as RAG knowledge base
│   ├── symptom_guidelines.json (future feature)
│
├── frontend/                  # Vite + React chat UI
│   ├── src/
│   ├── public/
│   └── ...
│
├── .env                       # API keys, model selection
├── .gitignore
├── requirements.txt
└── README.md

Getting Started
1. Clone the Repo
git clone https://github.com/BessyTan/healthdialog.git
cd healthdialog

2. Create & Activate Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Add API Key
Create a .env at project root:
OPENAI_API_KEY=sk-your-key-here
GPT_MODEL=gpt-4.1-mini

You can switch models easily (e.g., gpt-4o-mini, gpt-4.1, etc.)

5. Run Backend (FastAPI)
uvicorn src.app:app --reload

View API:
http://localhost:8000/
http://localhost:8000/health
http://localhost:8000/ask?query=What%20is%20hypertension%3F

6. Run Frontend (React)
cd frontend
npm install
npm run dev

Open browser:
http://localhost:5173

You now have a fully connected GPT-4 + FAISS medical triage assistant.

How the System Works
User Query
    ↓
FAISS Vector Store (sentence-transformer: all-MiniLM-L6-v2)
    ↓ top-k questions
Select relevant FAQ Q/A from clinical_faq.csv
    ↓
Construct “Clinical Sources” block for grounding
    ↓
GPT-4 synthesizes safe triage guidance
    ↓
Confidence = exp(–FAISS_distance)
Hallucination Risk = low/medium/high
    ↓
Frontend renders answer + sources + risk badges

API Documentation
GET /ask?query=...

Returns:

{
  "answer": "Your grounded triage answer from GPT-4",
  "confidence": 0.93,
  "hallucination_risk": "low",
  "sources": [
    {
      "title": "Clinical FAQ: What is hypertension?",
      "snippet": "Hypertension is high blood pressure.",
      "url": null
    }
  ]
}


If GPT-4 fails (timeout, rate limit, etc.), the system never crashes: It falls back to the nearest FAQ answer:
{
  "answer": "Hypertension is high blood pressure. (Fallback used)",
  "confidence": 0.88,
  "hallucination_risk": "low",
  "sources": [...]
}

Clinical Safety Rules
The GPT-4 prompt enforces:
Do:
    Use only retrieved clinical sources
    Provide simple, safe triage steps
    Recommend emergency care for red-flag symptoms

Don’t:
    Diagnose
    Invent facts
    Pretend to replace doctors
    Provide treatment plans
    Give medication advice
This keeps the assistant within a safe scope.