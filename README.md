# HealthDialog – LLM Health Triage Chatbot with RAG

A clinically grounded health chatbot using GPT-4 + RAG (FAISS, LangChain) with:
- Source-grounded response generation
- Hallucination detection
- Confidence scoring
- Clinical guideline retrieval
- FastAPI backend

### Features
RAG pipeline for safe, evidence-backed responses  
FAISS vector store with medical knowledge  
Hallucination detection using semantic similarity  
FastAPI endpoint for real-time use  

structure
healthdialog/
│
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── embed_store.py
│   ├── rag_pipeline.py
│   ├── evaluator.py
│   ├── hallucination_detector.py
│   ├── app.py
│
├── data/
│   ├── symptom_guidelines.json
│   ├── clinical_faq.csv
│
├── tests/
│   ├── test_rag.py
│   ├── test_detector.py
│
├── requirements.txt
├── README.md
└── .gitignore

---

## Run Locally
### 1. Install dependencies
pip install -r requirements.txt

### 2. Add your API key
Create `.env`:
OPENAI_API_KEY=your_key_here

### 3. Start API
uvicorn src.app:app --reload

---
## Example Query
GET localhost:8000/ask?query=I have chest pain what should I do?


