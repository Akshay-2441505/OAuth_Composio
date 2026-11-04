import json
import logging
from typing import Dict, Any, Tuple, Optional
from openai import AsyncOpenAI
from app.config import settings
from app.services.llm.base import LLMProvider
from app.services.llm.prompts import SYSTEM_PROMPT, build_research_prompt

logger = logging.getLogger("oauth_compass.groq")

class GroqAdapter(LLMProvider):
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL or "llama-3.3-70b-versatile"
        self.client = AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.api_key or "missing_key",
            timeout=settings.API_TIMEOUT_SECONDS,
        )

    @property
    def provider_name(self) -> str:
        return "groq"

    @property
    def model_name(self) -> str:
        return self.model

    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    async def generate_guide_json(
        self,
        evidence_package: Dict[str, Any],
        repair_feedback: Optional[str] = None
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        if not self.is_configured():
            return None, "Groq API key is not configured"

        user_prompt = build_research_prompt(evidence_package, repair_feedback)

        try:
            logger.info(f"Invoking Groq model '{self.model}'...")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
            )
            raw_text = response.choices[0].message.content or ""
            data = json.loads(raw_text)
            return data, None
        except json.JSONDecodeError as e:
            logger.warning(f"Groq returned invalid JSON: {e}")
            return None, f"JSONDecodeError: {str(e)}"
        except Exception as e:
            logger.error(f"Groq invocation failed: {e}")
            return None, f"GroqError: {str(e)}"

