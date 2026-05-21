# AgentForge Python Client

```bash
pip install agentforge-client
```

```python
from agentforge import Agent

# Create a free key
result = Agent.create_key("free")
key = result["api_key"]

# Use the agent
agent = Agent(api_key=key)
result = agent.execute(
    task="review this code",
    context="def hello(): print('hello')"
)
print(result['result'])
```
