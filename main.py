"""GreenPulse AI - FastAPI backend (Hour 1: health check + sample data)."""
import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .data_loader import build_payload, load_sample

app = FastAPI(title="GreenPulse AI API", version="0.1.0")

origins = [
    o.strip()
    for o in os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "greenpulse-ai-api"}


@app.get("/api/sample-data")
def sample_data(limit: int = Query(50, ge=1, le=500)) -> dict:
    try:
        return build_payload(load_sample(), limit=limit)
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=f"Could not load sample data: {exc}") from exc
