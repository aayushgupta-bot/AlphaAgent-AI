import os

class Settings:
    PROJECT_NAME: str = "AlphaAgent AI"
    PROJECT_VERSION: str = "1.0.0"
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

settings = Settings()
