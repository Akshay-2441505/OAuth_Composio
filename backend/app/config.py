import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), env_file_encoding="utf-8", extra="ignore")

    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./oauth_compass.db"
    FRONTEND_ORIGIN: str = "http://localhost:5173"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://localhost:5174"
    
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "meta-llama/llama-3.3-70b-instruct"
    
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    TAVILY_API_KEY: str = ""
    
    AI_PROVIDER_ORDER: str = "openrouter,groq"
    
    API_TIMEOUT_SECONDS: int = 60
    MAX_RESEARCH_PAGES: int = 8
    MAX_PAGE_BYTES: int = 1500000

    @property
    def provider_order(self) -> List[str]:
        return [p.strip() for p in self.AI_PROVIDER_ORDER.split(",") if p.strip()]

    @property
    def cors_origins_list(self) -> List[str]:
        origins = [orig.strip() for orig in self.CORS_ORIGINS.split(",") if orig.strip()]
        if self.FRONTEND_ORIGIN and self.FRONTEND_ORIGIN not in origins:
            origins.append(self.FRONTEND_ORIGIN)
        return origins

settings = Settings()
