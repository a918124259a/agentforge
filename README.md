# AgentForge ⚡

**AI Agent as a Service** — One API for intelligent agent capabilities.

> Deploy your own AI Agent API in 5 minutes. Code review, test generation, documentation writing, data analysis — all through a single API endpoint.

[![Deploy to Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square)](https://render.com/deploy?repo=https://github.com/a918124259a/agentforge)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Buy](https://img.shields.io/badge/Buy-Pro%20%2449-purple?style=flat-square)](https://a918124259a.github.io/agentforge/buy.html)

---

## ✦ Why AgentForge?

Most AI agent frameworks require complex setup, multiple dependencies, and deep infrastructure knowledge. AgentForge wraps everything into a **single FastAPI server** with one endpoint:

```
POST /v1/agent/execute
Authorization: Bearer <your-api-key>
{"task": "review this code", "context": "..."}
```

### Built-in Agents

| Agent | Task | Example |
|-------|------|---------|
| 🔍 **Code Review** | Automated code analysis & security scanning | `"review this pull request"` |
| 🧪 **Test Generator** | Generate unit/integration/E2E tests | `"generate tests for auth module"` |
| 📝 **Doc Writer** | Generate README, API docs, inline docs | `"write API documentation"` |
| 💬 **General Agent** | Custom tasks, analysis, Q&A | `"analyze this dataset"` |

### Smart Agent Routing

Just describe what you need — AgentForge automatically detects the task type and routes it to the best-suited agent with the right system prompt. No manual configuration needed.

---

## ✦ Quick Start (30 seconds)

```bash
# 1. Clone & install
git clone https://github.com/a918124259a/agentforge.git
cd agentforge/backend
pip install -r requirements.txt

# 2. Set your LLM key
export LLM_API_KEY="your-openai-or-deepseek-key"

# 3. Start
python main.py
# → http://localhost:8765
# → Docs: http://localhost:8765/docs
```

### Create an API Key

```bash
curl -X POST http://localhost:8765/v1/keys/create \
  -H "Content-Type: application/json" \
  -d '{"plan": "free"}'
# → {"api_key": "af_47e...380b", "plan": "free"}
```

### Execute an Agent Task

```bash
curl -X POST http://localhost:8765/v1/agent/execute \
  -H "Authorization: Bearer af_47e...380b" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "review this code",
    "context": "def add(a, b): return a + b",
    "format": "markdown"
  }'
```

---

## ✦ Deployment Options

### One-Click Deploy

| Platform | Command | Cost |
|----------|---------|------|
| **Render** | `bash deploy.sh render` | Free tier available |
| **Railway** | `bash deploy.sh railway` | $5 credit (free) |
| **Docker** | `docker-compose up -d` | Your own server |
| **Manual** | `python main.py` | Local dev |

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_API_KEY` | ✅ Yes | — | Your LLM provider API key |
| `LLM_BASE_URL` | No | `https://api.deepseek.com` | LLM API endpoint |
| `LLM_MODEL` | No | `deepseek-chat` | Model to use |
| `STRIPE_SECRET_KEY` | No | — | For Stripe payments |
| `STRIPE_PUBLISHABLE_KEY` | No | — | For Stripe payments |

---

## ✦ Pricing

Buy the full source code — deploy on your own infrastructure:

| Plan | Price | Includes |
|------|-------|----------|
| **Starter** | **$19** | Source code + deployment guide + 30 days support |
| **Pro** | **$49** | Source code + custom agent templates + 3 setup sessions + 90 days support |
| **Enterprise** | **$199** | Source code + custom agent development + white-label + 12 months support |

👉 **[Buy Now](https://a918124259a.github.io/agentforge/buy.html)**

---

## ✦ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │────▶│ AgentForge   │────▶│   LLM API   │
│ (curl/SDK)  │     │   API        │     │ (OpenAI/DS) │
└─────────────┘     │   :8765       │     └─────────────┘
                    │              │
                    │ ┌──────────┐ │
                    │ │ Task     │ │
                    │ │ Router   │ │
                    │ ├──────────┤ │
                    │ │ Review   │ │
                    │ │ Test     │ │
                    │ │ Doc      │ │
                    │ │ General  │ │
                    │ └──────────┘ │
                    └──────────────┘
```

### Python Client

```python
pip install agentforge-client
```

```python
from agentforge import Agent

agent = Agent(api_key="af_your_key")
result = agent.execute("review this code", context=code)
print(result['result'])
```

---

## ✦ Tech Stack

- **Backend:** Python 3.11+ · FastAPI · httpx · Uvicorn
- **AI:** OpenAI / DeepSeek / Claude / Any OpenAI-compatible API
- **Client:** Python SDK (pip install)
- **Deploy:** Docker · Render · Railway
- **Payments:** Stripe ready (or manual via Telegram)

---

## ✦ Project Structure

```
agentforge/
├── backend/
│   ├── main.py          # FastAPI server with all agents
│   ├── config.py        # Configuration & pricing plans
│   └── requirements.txt
├── web/
│   ├── index.html       # Landing page (GitHub Pages)
│   └── buy.html         # Pricing & purchase page
├── client/
│   └── agentforge/
│       └── __init__.py  # Python SDK
├── deploy.sh            # One-click deploy script
├── render.yaml          # Render config
├── docker-compose.yml   # Docker setup
└── README.md
```

---

## ✦ Roadmap

- [x] Core API with agent routing
- [x] Code Review agent
- [x] Test Generation agent
- [x] Documentation agent
- [x] API key management
- [x] Docker deployment
- [ ] Stripe payment integration
- [ ] Usage analytics dashboard
- [ ] Custom agent builder
- [ ] Claude Code / Copilot integration
- [ ] Webhook support

---

## ✦ License & Support

- **License:** MIT (free to use, modify, and sell)
- **Support:** [Telegram](https://t.me/liaodengwanbot)
- **Issues:** [GitHub Issues](https://github.com/a918124259a/agentforge/issues)

---

<p align="center">
  <b>Built with ❤️ by <a href="https://github.com/a918124259a">@a918124259a</a></b><br>
  <a href="https://a918124259a.github.io/agentforge/buy.html">Buy AgentForge →</a>
</p>
