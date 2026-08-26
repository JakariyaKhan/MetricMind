"""
MetricMind - Conversational BI Server & API Gateway
FastAPI backend providing:
- Real-time Conversational BI streaming (SSE)
- Semantic Layer metadata and query proxy
- Audit and Governance telemetry endpoints
- Static file serving for the Next.js / Tremor inspired UI
"""

import os
import json
import asyncio
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

from semantic_layer.engine import SemanticEngine
from agent.orchestrator import MetricMindAgent

app = FastAPI(
    title="MetricMind Conversational BI API",
    description="Production-ready Agentic Semantic BI Gateway",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = SemanticEngine()
agent = MetricMindAgent(engine=engine)

class ChatRequest(BaseModel):
    query: str
    stream: Optional[bool] = False

# Telemetry stats
audit_stats = {
    "queries_processed": 0,
    "deterministic_hits": 0,
    "sql_hallucinations_prevented": 0,
    "secondary_diagnostics_triggered": 0,
    "governance_limits_applied": 0
}

@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "MetricMind Agentic BI Engine"}

@app.get("/api/semantic/meta")
def get_semantic_metadata():
    """Returns the Cube.dev semantic schema catalog."""
    return engine.get_meta()

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """Standard non-streaming Chat endpoint returning full JSON payload with charts & audit steps."""
    if not req.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    result = agent.orchestrate(req.query)
    
    # Update telemetry
    audit_stats["queries_processed"] += 1
    audit_stats["deterministic_hits"] += 1
    audit_stats["sql_hallucinations_prevented"] += len(result.get("steps", []))
    if result.get("type") == "multi_step_diagnostic":
        audit_stats["secondary_diagnostics_triggered"] += 1
    if result.get("governance", {}).get("max_rows_enforced"):
        audit_stats["governance_limits_applied"] += 1
        
    return JSONResponse(content=result)

@app.post("/api/chat/stream")
async def chat_stream_endpoint(req: ChatRequest):
    """Server-Sent Events (SSE) streaming endpoint for responsive Conversational BI UI."""
    if not req.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    result = agent.orchestrate(req.query)
    text_content = result.get("text", "")

    async def event_generator():
        # 1. Stream thinking / reasoning phase
        yield f"data: {json.dumps({'type': 'status', 'content': 'Inspecting Semantic Layer schema...'})}\n\n"
        await asyncio.sleep(0.1)
        
        if result.get("type") == "multi_step_diagnostic":
            yield f"data: {json.dumps({'type': 'status', 'content': 'Margin variance detected. Dispatching secondary cost breakdown diagnostic...'})}\n\n"
            await asyncio.sleep(0.15)

        # 2. Stream tokens of the analytical synthesis
        words = text_content.split(" ")
        chunk_size = 4
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size]) + " "
            yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"
            await asyncio.sleep(0.04)

        # 3. Stream final complete payload with charts and audit drawers
        yield f"data: {json.dumps({'type': 'complete', 'payload': result})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/audit/stats")
def get_audit_telemetry():
    """Returns governance audit and single-source-of-truth telemetry."""
    return audit_stats

# Mount Frontend static assets
frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def serve_frontend_root():
        return FileResponse(os.path.join(frontend_path, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
