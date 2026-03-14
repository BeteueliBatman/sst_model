from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .agent import STTCorrectionAgent

app = FastAPI(title="Georgian STT Autocorrect Agent", version="0.1.0")
agent = STTCorrectionAgent()


class CorrectionRequest(BaseModel):
    text: str = Field(min_length=1, description="Raw Georgian STT text")


class CorrectionResponse(BaseModel):
    corrected_text: str
    model: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/correct", response_model=CorrectionResponse)
def correct(payload: CorrectionRequest) -> CorrectionResponse:
    try:
        result = agent.correct_text(payload.text)
        return CorrectionResponse(corrected_text=result.corrected_text, model=result.model)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc
