# src/embed_store.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingStore:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts: list[str] = []

    def build_index(self, texts):
        embeddings = self.model.encode(texts)
        embeddings = np.array(embeddings).astype("float32")
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        self.texts = list(texts)

    def query(self, query: str, top_k: int = 5):
        if self.index is None:
            raise RuntimeError("Index has not been built. Call build_index() first.")

        q_emb = self.model.encode([query])
        q_emb = np.array(q_emb).astype("float32")

        distances, idx = self.index.search(q_emb, top_k)
        indices = idx[0].tolist()
        dists = [float(d) for d in distances[0]]
        return indices, dists

    def get_text(self, idx: int) -> str:
        return self.texts[idx]
