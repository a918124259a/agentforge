# AgentForge ⚡

**AI Agent as a Service** — One API for intelligent agent capabilities.

🌐 **Landing Page:** https://a918124259a.github.io/agentforge/

## Quick Start

```bash
# Create an API key
curl -X POST https://api.agentforge.dev/v1/keys/create \
  -H "Content-Type: application/json" \
  -d '{"plan": "free"}'

# Execute an agent task
curl -X POST https://api.agentforge.dev/v1/agent/execute \
  -H "Authorization: Bearer af_your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "review this code",
    "context": "def add(a, b): return a + b",
    "format": "markdown"
  }'
```

## Features

- 🔍 **Code Review** — Automated code analysis and review
- 🧪 **Test Generation** — Generate unit/integration/E2E tests
- 📝 **Doc Writer** — Generate API docs and README files
- 📊 **Data Analysis** — Natural language data insights
- 🔄 **CI/CD Integration** — GitHub Actions, GitLab CI
- 🌐 **Custom Agents** — Define your own agent tools

## Python Client

```bash
pip install agentforge-client
```

```python
from agentforge import Agent
agent = Agent(api_key="af_your_key")
result = agent.execute("review this code", context=code)
print(result['result'])
```

## Tech Stack

- **Backend:** Python + FastAPI
- **Frontend:** HTML + Tailwind CSS
- **Deployment:** Docker / Railway / Vercel
- **Client:** Python + httpx

## Project Structure

```
agentforge/
├── backend/
│   ├── main.py          # FastAPI server
│   ├── config.py        # Configuration
│   └── requirements.txt
├── web/
│   └── index.html       # Landing page
├── client/
│   └── agentforge/
│       └── __init__.py  # Python client
├── index.html           # GitHub Pages root
├── docker-compose.yml
└── README.md
```

## License

MIT
