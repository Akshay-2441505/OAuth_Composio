from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional

class LLMProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        pass

    @abstractmethod
    async def generate_guide_json(
        self,
        evidence_package: Dict[str, Any],
        repair_feedback: Optional[str] = None
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Takes a normalized evidence package and returns:
        (parsed_dict_payload, error_message_if_any)
        """
        pass

