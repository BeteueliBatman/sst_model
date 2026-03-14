from __future__ import annotations

from contextlib import asynccontextmanager
import logging
import socket

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .agent import STTCorrectionAgent

logger = logging.getLogger("uvicorn.error")


def _resolve_lan_ip() -> str:
    """Best-effort LAN IP detection for startup logs and root endpoint."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"


@asynccontextmanager
async def lifespan(_: FastAPI):
    lan_ip = _resolve_lan_ip()
    logger.info("Open local demo: http://localhost:8000/docs")
    logger.info("Open API health: http://localhost:8000/health")
    logger.info("From another device on same network: http://%s:8000/docs", lan_ip)
    yield


app = FastAPI(title="Georgian STT Autocorrect Agent", version="0.1.0", lifespan=lifespan)
agent = STTCorrectionAgent()


class CorrectionRequest(BaseModel):
    text: str = Field(min_length=1, description="Raw Georgian STT text")


class CorrectionResponse(BaseModel):
    corrected_text: str
    model: str


@app.get("/")
def home() -> dict[str, str]:
    lan_ip = _resolve_lan_ip()
    return {
        "message": "Server is running. Open /docs for interactive demo.",
        "local_docs": "http://localhost:8000/docs",
        "local_health": "http://localhost:8000/health",
        "lan_docs": f"http://{lan_ip}:8000/docs",
    }


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
