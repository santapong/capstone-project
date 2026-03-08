import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "CapStone-Project"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/"
    
    # AI Models
    LLM_MODEL: str = "typhoon-v1.5x-70b-instruct"
    MODEL_PROVIDER: str = "openai"
    MODEL_BASE_URL: str = "https://api.opentyphoon.ai/v1"
    TYPHOON_API_KEY: Optional[str] = None
    EMBEDDING_MODEL: str = "bge-m3"
    TEMPERATURE: float = 0.0
    
    # External APIs
    LANGSMITH_API_KEY: Optional[str] = None
    GOOGLE_CSE_ID: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # Database - RAG (ChromaDB)
    COLLECTION_NAME: str = "langchain"
    PERSIST_DIR: str = "database/vector_history"
    
    # Database - Metadata (SQLAlchemy)
    PYTHONPATH: str = "."
    DATABASE_URL: Optional[str] = None
    
    @property
    def sqlalchemy_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # Default to SQLite if no DATABASE_URL is provided
        return f"sqlite:///{self.PYTHONPATH}/database/history_database/internal.db"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_PATH: str = "app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
