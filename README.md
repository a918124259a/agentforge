# AgentForge

AI Agent as a Service — One API for intelligent agent capabilities.

## Quick Start

```bash
# Start the API
cd backend && pip install -r requirements.txt && python main.py

# Open landing page
open web/index.html
```

## API

```
POST /v1/agent/execute
  Headers: Authorization: Bearer <your_key>
  Body: {"task": "...", "context": "...", "format": "text"}

POST /v1/keys/create
  Body: {"plan": "free|starter|pro|enterprise"}

GET  /v1/usage
  Headers: Authorization: Bearer <your_key>
```

## Deploy

```bash
docker-compose up -d
```
