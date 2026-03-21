"""
AI Assistant Firewall — FastAPI Backend v3.0
Engine: HuggingFace AI + Rule-based detection
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sqlite3, os

from hybrid_engine import HybridEngine

app = FastAPI(title="AI Assistant Firewall", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

engine = HybridEngine(hf_key=os.environ.get("HF_API_KEY"))

DB_PATH = "firewall.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS prompt_logs (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt        TEXT NOT NULL,
                risk_score    REAL NOT NULL,
                status        TEXT NOT NULL,
                reason        TEXT NOT NULL,
                analysis_mode TEXT DEFAULT 'rules_only',
                threat_type   TEXT,
                ai_reasoning  TEXT,
                timestamp     TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()


class PromptRequest(BaseModel):
    prompt: str

# Use Optional[str] instead of str | None for Python 3.9 compatibility
class PromptResponse(BaseModel):
    prompt:        str
    risk_score:    float
    status:        str
    reason:        str
    analysis_mode: str
    threat_type:   Optional[str]
    ai_reasoning:  Optional[str]
    timestamp:     str


@app.post("/check-prompt", response_model=PromptResponse)
def check_prompt(req: PromptRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        result    = engine.analyze(req.prompt)
        timestamp = datetime.utcnow().isoformat()

        with get_db() as conn:
            conn.execute(
                """INSERT INTO prompt_logs
                   (prompt, risk_score, status, reason, analysis_mode, threat_type, ai_reasoning, timestamp)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (result["prompt"], result["risk_score"], result["status"], result["reason"],
                 result["analysis_mode"], result.get("threat_type"), result.get("ai_reasoning"), timestamp),
            )
            conn.commit()

        return PromptResponse(**result, timestamp=timestamp)

    except Exception as e:
        print(f"[ERROR] /check-prompt crashed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs")
def get_logs():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM prompt_logs ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]


@app.delete("/logs")
def clear_logs():
    with get_db() as conn:
        conn.execute("DELETE FROM prompt_logs")
        conn.commit()
    return {"message": "Logs cleared"}


@app.get("/status")
def get_status():
    return {
        "version":    "3.0.0",
        "ai_mode":    engine.ai_mode,
        "ai_enabled": engine.ai_available,
        "model":      engine.model_name,
        "mode_label": f"🤗 HuggingFace ({engine.model_name})" if engine.ai_available else "⚙ Rules Only",
    }


@app.get("/")
def root():
    return {"message": "AI Firewall v3.0", "ai_mode": engine.ai_mode, "docs": "/docs"}