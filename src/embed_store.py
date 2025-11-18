import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingStore:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []

    def build_index(self, texts):
        embeddings = self.model.encode(texts)
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts = texts

    def query(self, query, top_k=5):
        q_emb = self.model.encode([query])
        distances, idx = self.index.search(q_emb.astype("float32"), top_k)
        return [self.texts[i] for i in idx[0]]
