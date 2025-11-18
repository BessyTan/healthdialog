from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class HallucinationDetector:
    def __init__(self, model="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model)

    def detect(self, query, response, threshold=0.4):
        q_emb = self.model.encode([query])
        r_emb = self.model.encode([response])
        score = cosine_similarity(q_emb, r_emb)[0][0]
        return score < threshold  # True = hallucination
