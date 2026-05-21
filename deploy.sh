#!/bin/bash
# AgentForge Deployment Script
# Deploy to Railway or Render with one command

set -e

echo "🚀 AgentForge Deployment"
echo "========================"

deploy_render() {
    echo "📦 Deploying to Render..."
    echo "1. Go to https://dashboard.render.com/select-repo"
    echo "2. Select: a918124259a/agentforge"
    echo "3. Service type: Web Service"
    echo "4. Root Directory: backend"
    echo "5. Build Command: pip install -r requirements.txt"
    echo "6. Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
    echo "7. Free tier: ✓"
    echo ""
    echo "🌐 Landing page: https://a918124259a.github.io/agentforge/"
    echo "📡 API: https://agentforge-api.onrender.com"
}

deploy_railway() {
    echo "📦 Deploying to Railway..."
    echo "1. Go to https://railway.app/new"
    echo "2. Select: Deploy from GitHub repo"
    echo "3. Choose: a918124259a/agentforge"
    echo "4. Root Directory: backend"
    echo "5. Start Command: python main.py"
    echo "6. Free tier: ✓ (\$5 credit)"
    echo ""
    echo "🌐 Landing page: https://a918124259a.github.io/agentforge/"
}

deploy_local() {
    echo "📦 Deploying locally..."
    cd "$(dirname "$0")/backend"
    pip install -r requirements.txt
    echo "✅ Running on http://localhost:8765"
    echo "📘 Docs: http://localhost:8765/docs"
    python main.py
}

case "${1:-local}" in
    render) deploy_render ;;
    railway) deploy_railway ;;
    local) deploy_local ;;
    *) echo "Usage: $0 {render|railway|local}" ;;
esac
