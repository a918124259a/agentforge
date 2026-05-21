"""AgentForge Python Client"""
import json, os
from typing import Optional
import httpx

class Agent:
    """AgentForge AI Agent client."""
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:8765"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
    
    def execute(self, task: str, context: str = "", format: str = "markdown") -> dict:
        """Execute an agent task."""
        resp = httpx.post(
            f"{self.base_url}/v1/agent/execute",
            json={"task": task, "context": context, "format": format},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        resp.raise_for_status()
        return resp.json()
    
    def usage(self) -> dict:
        """Get usage stats."""
        resp = httpx.get(
            f"{self.base_url}/v1/usage",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def create_key(plan: str = "free", base_url: str = "http://localhost:8765") -> dict:
        """Create a new API key."""
        resp = httpx.post(
            f"{base_url}/v1/keys/create",
            json={"plan": plan}
        )
        resp.raise_for_status()
        return resp.json()

    def __repr__(self):
        return f"Agent(key={self.api_key[:8]}..., url={self.base_url})"


# Example usage
if __name__ == "__main__":
    # Create a key
    result = Agent.create_key("starter")
    key = result["api_key"]
    print(f"🔑 Created key: {key[:12]}...")
    
    # Use it
    agent = Agent(api_key=key)
    result = agent.execute("generate tests for a Python calculator class")
    print(f"✅ Result:\n{result['result'][:200]}...")
    
    # Check usage
    usage = agent.usage()
    print(f"📊 Usage: {usage}")
