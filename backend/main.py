"""
AgentForge API — AI Agent as a Service
"""
import os, json, hashlib, time, hmac, uuid
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import httpx


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
async def execute_agent(req: AgentRequest, api_key: str = Depends(verify_api_key)):
    """Execute an AI agent task."""
    start = time.time()
    
    task_id = f"task_{uuid.uuid4().hex[:12]}"
    result = await process_task(req.task, req.context)
    
    duration = int((time.time() - start) * 1000)
    tokens = estimate_tokens(req.task) + estimate_tokens(result)
    
    API_KEYS[api_key]["usage"] += 1
    
    return {
        "id": task_id,
        "result": result,
        "format": req.format,
        "tokens_used": tokens,
        "duration_ms": duration
    }

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

# --- LLM Integration ---

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://inference-api.nousresearch.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek/deepseek-v4-flash")

async def call_llm(prompt: str, system: str = "") -> str:
    """Call the LLM API to process a prompt."""
    if not LLM_API_KEY:
        return "[Mock] LLM not configured. Set LLM_API_KEY env var."
    
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            resp = await client.post(
                f"{LLM_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"},
                json={"model": LLM_MODEL, "messages": messages, "max_tokens": 4096}
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"⚠️ LLM call failed: {str(e)}\n\nFalling back to template response.\n\n---\n\n## Task Analysis\n\n**Task:** {prompt[:200]}\n**Context length:** {len(prompt)} chars\n\nThis agent is currently in demo mode. Set LLM_API_KEY environment variable to enable real AI processing.\n\n**Demo Response:**\nYour request has been received by AgentForge. To get real AI-powered results:\n1. Set LLM_API_KEY env var\n2. Or use the hosted version at api.agentforge.dev\n3. Or contact us for a demo key"

AGENT_SYSTEM_PROMPTS = {
    "review": """You are an expert code reviewer. Analyze code for:
1. Bugs and logic errors
2. Security vulnerabilities
3. Performance issues
4. Best practice violations
5. Code quality and readability

Return a structured markdown report with severity levels (🔴 Critical, 🟡 Warning, 💡 Suggestion).""",

    "test": """You are a test generation expert. Generate comprehensive tests.
For each test include: test name, description, and the actual test code.
Use the testing framework appropriate for the language shown.""",

    "doc": """You are a technical documentation expert. Generate clear, concise documentation.
Include: overview, installation, usage examples, API reference, and configuration options.""",

    "general": """You are a helpful AI agent. Complete the user's task accurately and thoroughly.
Provide clear, actionable responses with code examples where relevant."""
}

async def process_task(task: str, context: str = "") -> str:
    """Route task to appropriate agent and process with LLM."""
    task_lower = task.lower()
    
    if any(w in task_lower for w in ["review", "code review", "audit"]):
        system = AGENT_SYSTEM_PROMPTS["review"]
        prompt = f"## Code to Review\n\n{context or task}\n\nReview the above code and provide detailed feedback."
    elif any(w in task_lower for w in ["test", "unit test", "integration test"]):
        system = AGENT_SYSTEM_PROMPTS["test"]
        prompt = f"## Code to Test\n\n{context or task}\n\nGenerate comprehensive tests for the above code."
    elif any(w in task_lower for w in ["doc", "document", "readme"]):
        system = AGENT_SYSTEM_PROMPTS["doc"]
        prompt = f"## Code to Document\n\n{context or task}\n\nGenerate documentation for the above code."
    else:
        system = AGENT_SYSTEM_PROMPTS["general"]
        prompt = f"## Task\n\n{task}\n\n## Context\n\n{context}\n\nComplete this task."
    
    return await call_llm(prompt, system)

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
