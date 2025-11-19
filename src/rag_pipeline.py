# src/rag_pipeline.py
from typing import Any, Dict
import math


class RAGPipeline:
    def __init__(self, embed_store, faq_df):
        """
        embed_store: EmbeddingStore
        faq_df: pandas DataFrame with 'question' and 'answer' columns
        """
        self.embed_store = embed_store
        self.faq_df = faq_df.reset_index(drop=True)

    def generate(self, query: str) -> Dict[str, Any]:
        """
        Lightweight RAG: use FAISS to find nearest FAQ question and return its answer.
        No external LLM, no OpenAI key required.
        """

        # 1. Retrieve nearest FAQs
        try:
            indices, distances = self.embed_store.query(query, top_k=3)
        except Exception as e:
            # If FAISS/index has an issue, fall back gracefully
            return {
                "answer": (
                    "I'm having trouble accessing my knowledge base right now. "
                    "Please try again later or consult a healthcare professional."
                ),
                "confidence": 0.0,
                "hallucination_risk": "high",
                "sources": [],
                "error": str(e),
            }

        # Filter out invalid indices
        valid = [(i, d) for i, d in zip(indices, distances) if 0 <= i < len(self.faq_df)]

        if not valid:
            return {
                "answer": (
                    "I don't have enough information in my FAQ data to answer that reliably. "
                    "Please consult a healthcare professional."
                ),
                "confidence": 0.2,
                "hallucination_risk": "medium",
                "sources": [],
            }

        # 2. Best match is the first result
        best_idx, best_dist = valid[0]
        row = self.faq_df.iloc[best_idx]
        q = str(row["question"])
        a = str(row["answer"])

        # 3. Build context & sources
        sources = []
        for idx, dist in valid:
            r = self.faq_df.iloc[idx]
            qq = str(r["question"])
            aa = str(r["answer"])
            sources.append(
                {
                    "title": f"Clinical FAQ: {qq}",
                    "snippet": aa,
                    "url": None,
                }
            )

        # 4. Turn FAISS distance into a rough confidence
        #    (smaller distance -> higher similarity -> higher confidence)
        #    This is a heuristic; adjust as you like.
        # avoid log(0)
        d = max(best_dist, 1e-6)
        # map distance to [0,1] with a simple decay
        confidence = math.exp(-d)
        confidence = float(max(0.0, min(1.0, confidence)))

        if confidence >= 0.8:
            risk = "low"
        elif confidence >= 0.4:
            risk = "medium"
        else:
            risk = "high"

        answer_text = a

        return {
            "answer": answer_text,
            "confidence": confidence,
            "hallucination_risk": risk,
            "sources": sources,
        }
