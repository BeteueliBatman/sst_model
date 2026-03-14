from __future__ import annotations

from dataclasses import dataclass

from .config import Settings
from .ollama_client import OllamaClient
from .prompts import SYSTEM_PROMPT, build_user_prompt


@dataclass(slots=True)
class CorrectionResult:
    raw_text: str
    corrected_text: str
    model: str


class STTCorrectionAgent:
    def __init__(self, settings: Settings | None = None, client: OllamaClient | None = None) -> None:
        self.settings = settings or Settings()
        self.client = client or OllamaClient(
            base_url=self.settings.ollama_base_url,
            timeout_s=self.settings.request_timeout_s,
        )

    def correct_text(self, raw_text: str) -> CorrectionResult:
        cleaned = raw_text.strip()
        if not cleaned:
            return CorrectionResult(raw_text=raw_text, corrected_text="", model=self.settings.model_name)

        corrected = self.client.generate(
            model=self.settings.model_name,
            system_prompt=SYSTEM_PROMPT,
            user_prompt=build_user_prompt(cleaned),
            temperature=self.settings.temperature,
        )

        return CorrectionResult(raw_text=raw_text, corrected_text=corrected, model=self.settings.model_name)
