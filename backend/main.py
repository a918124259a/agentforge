"""
AgentForge API — AI Agent as a Service
"""
import os, json, hashlib, time, hmac, uuid
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="AgentForge API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (MVP only)
API_KEYS = {}  # key -> {plan, usage, created_at}
USAGE_LOG = []  # {api_key, endpoint, timestamp, tokens_used}

class AgentRequest(BaseModel):
    task: str
    context: Optional[str] = ""
    format: Optional[str] = "text"  # text, json, markdown

class AgentResponse(BaseModel):
    id: str
    result: str
    format: str
    tokens_used: int
    duration_ms: int

def generate_api_key():
    return f"af_{uuid.uuid4().hex}"

def verify_api_key(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing API key")
    key = authorization.replace("Bearer ", "")
    if key not in API_KEYS:
        raise HTTPException(401, "Invalid API key")
    return key

@app.get("/")
def root():
    return {"service": "AgentForge", "version": "0.1.0", "status": "operational"}

@app.post("/v1/agent/execute")
def execute_agent(req: AgentRequest, api_key: str = Depends(verify_api_key)):
    """Execute an AI agent task."""
    start = time.time()
    
    # Simple AI execution using available model
    # For MVP: we'll integrate with the Hermes API or direct model calls
    task_id = f"task_{uuid.uuid4().hex[:12]}"
    
    # Simulate processing (will be replaced with real AI model call)
    result = process_task(req.task, req.context)
    
    duration = int((time.time() - start) * 1000)
    tokens = estimate_tokens(req.task) + estimate_tokens(result)
    
    # Log usage
    API_KEYS[api_key]["usage"] += 1
    
    return AgentResponse(
        id=task_id,
        result=result,
        format=req.format,
        tokens_used=tokens,
        duration_ms=duration
    )

@app.post("/v1/keys/create")
def create_key(plan: str = "free"):
    """Create a new API key."""
    key = generate_api_key()
    API_KEYS[key] = {
        "plan": plan,
        "usage": 0,
        "created_at": time.time(),
        "key_prefix": key[:12]
    }
    return {"api_key": key, "plan": plan, "message": "Store this key securely - it won't be shown again"}

@app.get("/v1/usage")
def get_usage(api_key: str = Depends(verify_api_key)):
    """Get usage statistics for your API key."""
    info = API_KEYS[api_key]
    return {
        "plan": info["plan"],
        "total_requests": info["usage"],
        "created_at": info["created_at"]
    }

# --- Internal helpers ---

def process_task(task: str, context: str = "") -> str:
    """Process a task using AI. MVP: simple template-based responses."""
    task_lower = task.lower()
    
    if "code review" in task_lower or "review" in task_lower:
        return f"""## Code Review Results

**Issues Found:**
1. ⚠️ Potential null pointer at line 42 — variable may be uninitialized
2. 💡 Consider using async/await instead of callbacks (line 78)
3. ✅ Error handling is well implemented (lines 100-120)

**Summary:** 1 critical, 2 warnings, 3 suggestions"""
    
    if "test" in task_lower or "generate test" in task_lower:
        return """```typescript
import { describe, it, expect } from 'vitest';

describe('UserService', () => {
  it('should create a new user', async () => {
    const user = await UserService.create({ name: 'Test' });
    expect(user.id).toBeDefined();
    expect(user.name).toBe('Test');
  });

  it('should reject duplicate emails', async () => {
    await UserService.create({ email: 'test@test.com' });
    await expect(
      UserService.create({ email: 'test@test.com' })
    ).rejects.toThrow('Email already exists');
  });
});
```"""
    
    if "summarize" in task_lower or "summary" in task_lower:
        return f"""## Summary

Based on the provided context, here are the key points:
1. Main topic: {task[:50]}...
2. Actionable insights identified
3. Recommendations provided below

*This is an AI-generated summary. Please verify critical information.*"""
    
    # Default: general response
    return f"""Task processed: {task[:100]}

**Result:**
The agent has analyzed your request and prepared the following output.
For more specific tasks, please use one of: "review", "generate test", "summarize" keywords in your task description."""

def estimate_tokens(text: str) -> int:
    """Rough token estimation."""
    return len(text.split()) + len(text) // 10

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": time.time()}

if __name__ == "__main__":
    print("🚀 AgentForge API starting...")
    print(f"   Docs: http://localhost:8765/docs")
    uvicorn.run(app, host="0.0.0.0", port=8765)
