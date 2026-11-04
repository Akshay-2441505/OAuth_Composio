import logging
from typing import Dict, Any, Tuple, Optional
from pydantic import ValidationError

from app.config import settings
from app.schemas.guide import GuideSchema
from app.services.llm.base import LLMProvider
from app.services.llm.openrouter import OpenRouterAdapter
from app.services.llm.groq import GroqAdapter

logger = logging.getLogger("oauth_compass.llm_router")

class LLMRouter:
    def __init__(self):
        self.providers: Dict[str, LLMProvider] = {
            "openrouter": OpenRouterAdapter(),
            "groq": GroqAdapter(),
        }

    async def generate_structured_guide(
        self,
        evidence_package: Dict[str, Any]
    ) -> Tuple[Optional[GuideSchema], Optional[str], Optional[str], Optional[str]]:
        """
        Attempts guide generation across configured providers in priority order.
        Validates with Pydantic; performs one repair attempt if validation fails.
        Returns: (validated_guide, provider_used, model_used, fallback_reason)
        """
        order = settings.provider_order
        fallback_reasons = []

        for provider_key in order:
            provider = self.providers.get(provider_key)
            if not provider:
                continue

            if not provider.is_configured():
                fallback_reasons.append(f"{provider_key}: not configured (missing API key)")
                continue

            logger.info(f"Attempting generation with provider '{provider.provider_name}' ({provider.model_name})...")
            
            # First attempt with this provider
            data, err = await provider.generate_guide_json(evidence_package)
            
            if err or not data:
                fallback_reasons.append(f"{provider_key}: {err}")
                logger.warning(f"Provider {provider_key} failed: {err}. Proceeding to fallback...")
                continue

            # Validate with Pydantic
            try:
                guide = GuideSchema.model_validate(data)
                return guide, provider.provider_name, provider.model_name, (", ".join(fallback_reasons) if fallback_reasons else None)
            except ValidationError as ve:
                logger.warning(f"Schema validation failed on {provider_key} output: {ve}. Attempting one repair retry...")
                # One repair retry
                repair_feedback = str(ve)
                repair_data, repair_err = await provider.generate_guide_json(evidence_package, repair_feedback=repair_feedback)
                if repair_data:
                    try:
                        repaired_guide = GuideSchema.model_validate(repair_data)
                        return repaired_guide, provider.provider_name, provider.model_name, (", ".join(fallback_reasons) if fallback_reasons else None)
                    except ValidationError as ve2:
                        fallback_reasons.append(f"{provider_key}: validation failed after repair ({ve2})")
                else:
                    fallback_reasons.append(f"{provider_key}: repair attempt failed ({repair_err})")

        error_summary = " | ".join(fallback_reasons) if fallback_reasons else "No LLM providers configured"
        logger.warning(f"All LLM providers exhausted: {error_summary}")
        
        return None, None, None, error_summary

llm_router = LLMRouter()

