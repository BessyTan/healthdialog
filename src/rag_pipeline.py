from langchain_openai import ChatOpenAI
from .hallucination_detector import HallucinationDetector
from .config import settings

class RAGPipeline:
    def __init__(self, embed_store):
        self.model = ChatOpenAI(model=settings.GPT_MODEL, temperature=0)
        self.embed_store = embed_store
        self.detector = HallucinationDetector()

    def generate(self, query):
        # Retrieve supporting documents
        docs = self.embed_store.query(query)
        context = "\n".join([f"- {d}" for d in docs])

        # Source-grounded prompt
        prompt = f"""
You are a medical triage assistant. Ground all responses in the clinical sources provided.
If information is missing, say "I don't have enough information to answer reliably."

Clinical Sources:
{context}

User Query: {query}

Respond with medically safe, concise guidance.
"""

        response = self.model.invoke(prompt).content

        # Hallucination detection
        hallucinated = self.detector.detect(query, response)

        return {
            "response": response,
            "hallucinated": hallucinated,
            "confidence": 1.0 - float(hallucinated),
            "sources": docs
        }
