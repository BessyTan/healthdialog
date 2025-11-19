# src/rag_pipeline.py
from typing import Any, Dict
import math

from langchain_openai import ChatOpenAI

from .config import settings  # <-- use Settings to get key & model


class RAGPipeline:
    def __init__(self, embed_store, faq_df):
        """
        embed_store: EmbeddingStore (FAISS + SentenceTransformer)
        faq_df: pandas DataFrame with 'question' and 'answer' columns
        """
        self.embed_store = embed_store
        self.faq_df = faq_df.reset_index(drop=True)

        # Explicitly pass api_key so we don't rely on OPENAI_API_KEY env var
        self.llm = ChatOpenAI(
            model=settings.GPT_MODEL,
            temperature=0,
            api_key=settings.OPENAI_API_KEY,
        )

    def _confidence_from_distance(self, dist: float) -> float:
        d = max(dist, 1e-6)
        conf = math.exp(-d)
        return float(max(0.0, min(1.0, conf)))

    def _risk_from_confidence(self, confidence: float) -> str:
        if confidence >= 0.8:
            return "low"
        elif confidence >= 0.4:
            return "medium"
        else:
            return "high"

    def generate(self, query: str) -> Dict[str, Any]:
        # 1. Retrieve nearest FAQ rows
        try:
            indices, distances = self.embed_store.query(query, top_k=3)
        except Exception as e:
            return {
                "answer": (
                    "I'm having trouble accessing my clinical knowledge base right now. "
                    "Please try again later or consult a healthcare professional."
                ),
                "confidence": 0.0,
                "hallucination_risk": "high",
                "sources": [],
                "error": f"retrieval_error: {e!s}",
            }

        valid = [(i, d) for i, d in zip(indices, distances)
                 if 0 <= i < len(self.faq_df)]

        if not valid:
            return {
                "answer": (
                    "I don't have enough information in my clinical FAQ data to answer that reliably. "
                    "Please consult a healthcare professional."
                ),
                "confidence": 0.2,
                "hallucination_risk": "medium",
                "sources": [],
            }

        best_idx, best_dist = valid[0]
        best_row = self.faq_df.iloc[best_idx]
        best_q = str(best_row["question"])
        best_a = str(best_row["answer"])

        context_blocks = []
        sources = []

        for idx, dist in valid:
            row = self.faq_df.iloc[idx]
            q = str(row["question"])
            a = str(row["answer"])
            context_blocks.append(f"Q: {q}\nA: {a}")
            sources.append(
                {
                    "title": f"Clinical FAQ: {q}",
                    "snippet": a,
                    "url": None,
                }
            )

        context_text = "\n\n---\n\n".join(context_blocks)

        prompt = f"""
You are a cautious medical triage assistant for laypersons.
You MUST ground all responses in the clinical sources provided below.

If the sources do not contain enough information to answer safely,
you MUST say: "I don't have enough information to answer reliably."
You are NOT a doctor and you do NOT provide a diagnosis.

Clinical Sources:
{context_text}

User Query:
{query}

Instructions:
- Use only the information from the clinical sources where possible.
- If a symptom sounds like an emergency (e.g. chest pain, difficulty breathing, stroke signs),
  clearly say to seek emergency care or call local emergency services.
- Keep the answer concise, clear, and in plain language.
- Avoid speculation beyond the sources.
"""

        fallback_used = False

        try:
            llm_resp = self.llm.invoke(prompt)
            answer_text = getattr(llm_resp, "content", str(llm_resp))
        except Exception as e:
            answer_text = (
                f"{best_a}\n\n"
                "(Note: I could not synthesize a full answer right now, so I'm showing "
                "the closest FAQ entry instead.)"
            )
            fallback_used = True

        confidence = self._confidence_from_distance(best_dist)
        risk = self._risk_from_confidence(confidence)

        return {
            "answer": answer_text,
            "confidence": confidence,
            "hallucination_risk": risk,
            "sources": sources,
            "fallback_used": fallback_used,
            "faiss_best_question": best_q,
            "faiss_best_answer": best_a,
        }
