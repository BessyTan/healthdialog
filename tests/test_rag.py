from embed_store import EmbeddingStore
from rag_pipeline import RAGPipeline

def test_rag_basic():
    store = EmbeddingStore("sentence-transformers/all-MiniLM-L6-v2")
    store.build_index(["Chest pain guidance", "Fever symptoms"])
    rag = RAGPipeline(store)

    res = rag.generate("What should I do if I have chest pain?")
    assert "response" in res
    assert len(res["sources"]) > 0
