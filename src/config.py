import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    GPT_MODEL = "gpt-4o"

settings = Settings()
