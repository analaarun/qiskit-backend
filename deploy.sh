#!/bin/bash

# One-command deployment script for Render
# Just run: ./deploy.sh

echo "🚀 Deploying Qiskit Backend to Render"
echo "======================================"
echo ""

# Check if in correct directory
if [ ! -f "server.py" ]; then
    echo "❌ Error: server.py not found!"
    echo "   Please run this script from the qiskit-backend directory"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Qiskit stateful backend"
    echo "✅ Git initialized"
    echo ""
fi

# Check if Render CLI is installed
if ! command -v render &> /dev/null; then
    echo "❌ Render CLI not found!"
    echo ""
    echo "Please install it:"
    echo "  npm install -g @render/cli"
    echo "  OR"
    echo "  brew install render"
    echo ""
    echo "Then run: render login"
    exit 1
fi

# Deploy to Render
echo "🚀 Deploying to Render..."
echo "   This will take 5-10 minutes (installing Qiskit)"
echo ""

render deploy

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Copy your Render URL from above"
    echo "   2. Test it: curl https://YOUR-URL.onrender.com/health"
    echo "   3. Update your HTML visualizer with the URL"
    echo ""
else
    echo ""
    echo "❌ Deployment failed!"
    echo ""
    echo "Troubleshooting:"
    echo "   1. Make sure you're logged in: render login"
    echo "   2. Check logs: render logs"
    echo "   3. Try dashboard: https://dashboard.render.com"
    echo ""
fi
