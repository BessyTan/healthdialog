# src/app.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .embed_store import EmbeddingStore
from .rag_pipeline import RAGPipeline
from .data_loader import load_clinical_faq

import os

app = FastAPI(title="HealthDialog API")

# CORS for React dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build vector store on startup from clinical_faq.csv
faq_df = load_clinical_faq()
texts = faq_df["question"].astype(str).tolist()

store = EmbeddingStore("sentence-transformers/all-MiniLM-L6-v2")
store.build_index(texts)

pipeline = RAGPipeline(store, faq_df)


@app.get("/")
def root():
    return {"message": "HealthDialog API is running!"}


@app.get("/health")
def health():
    return {"status": "ok", "faq_count": int(len(faq_df))}


@app.get("/ask")
def ask(query: str = Query(..., description="User symptom or question")):
    result = pipeline.generate(query)

    # enforce frontend shape + JSON-safe types
    answer = str(result.get("answer", ""))
    confidence = result.get("confidence", None)
    if confidence is not None:
        confidence = float(confidence)

    hallucination_risk = result.get("hallucination_risk", None)
    sources = result.get("sources", [])

    return {
        "answer": answer,
        "confidence": confidence,
        "hallucination_risk": hallucination_risk,
        "sources": sources,
    }
