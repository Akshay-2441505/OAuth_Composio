from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/api", tags=["health"])

@router.get("/health")
def get_health():
    return {
        "status": "ok",
        "app_env": settings.APP_ENV,
        "providers_configured": {
            "openrouter": bool(settings.OPENROUTER_API_KEY),
            "groq": bool(settings.GROQ_API_KEY),
            "tavily": bool(settings.TAVILY_API_KEY),
        },
        "provider_order": settings.provider_order,
    }

