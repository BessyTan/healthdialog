from fastapi import FastAPI
from .embed_store import EmbeddingStore
from .rag_pipeline import RAGPipeline
from .data_loader import load_clinical_faq

app = FastAPI()

# Build vector store on startup
faq_data = load_clinical_faq()
texts = faq_data['question'].tolist()
answers = faq_data['answer'].tolist()

store = EmbeddingStore("sentence-transformers/all-MiniLM-L6-v2")
store.build_index(texts)

pipeline = RAGPipeline(store)

@app.get("/")
def root():
    return {"message": "HealthDialog API is running!"}

@app.get("/ask")
def ask(query: str):
    return pipeline.generate(query)
