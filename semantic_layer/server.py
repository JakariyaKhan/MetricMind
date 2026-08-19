"""
MetricMind - Semantic Layer REST API Server
Provides Cube.dev-compatible endpoints:
- GET /cubejs-api/v1/meta
- POST /cubejs-api/v1/load
- POST /cubejs-api/v1/sql
"""

import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from semantic_layer.engine import SemanticEngine

app = FastAPI(
    title="MetricMind Semantic Layer API",
    description="Cube.dev-compatible governed Semantic Layer REST API",
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

class QueryPayload(BaseModel):
    query: Dict[str, Any]

@app.get("/cubejs-api/v1/meta")
def get_metadata():
    """Returns the complete metadata schema of cubes, dimensions, and measures."""
    return engine.get_meta()

@app.post("/cubejs-api/v1/load")
def load_query(payload: QueryPayload):
    """Executes a governed semantic query and returns deterministic JSON data."""
    try:
        result = engine.execute_query(payload.query)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cubejs-api/v1/load")
def load_query_get(query: str):
    """GET variant of load query accepting JSON-encoded query string parameter."""
    try:
        parsed_query = json.loads(query)
        result = engine.execute_query(parsed_query)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cubejs-api/v1/sql")
def get_sql(payload: QueryPayload):
    """Compiles and returns the exact SQL without executing it."""
    try:
        sql, params, _ = engine.compile_sql(payload.query)
        return {
            "sql": {
                "sql": [sql, params]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("semantic_layer.server:app", host="0.0.0.0", port=4000, reload=True)
