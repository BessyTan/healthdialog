# src/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GPT_MODEL: str = "gpt-4.1-mini"

    # Optional – if you had these in your .env, they won't break things:
    FASTAPI_HOST: str | None = None
    FASTAPI_PORT: int | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"  # <-- ignore unexpected env vars instead of crashing


settings = Settings()
