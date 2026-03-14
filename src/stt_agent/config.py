from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "qwen2.5:3b-instruct"
    request_timeout_s: float = 60.0
    temperature: float = 0.1
