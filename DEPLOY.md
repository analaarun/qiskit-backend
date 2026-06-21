# Deployment Guide - Render CLI

## Prerequisites

✅ Render CLI installed and authenticated (you've done this!)
✅ Git initialized in this directory

---

## Step 1: Test Locally First

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

Open another terminal and test:
```bash
./test_local.sh
```

You should see health checks, session creation, and Bell state execution!

---

## Step 2: Initialize Git Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Qiskit backend server"
```

---

## Step 3: Deploy to Render

### Option A: Deploy with Render CLI (Recommended)

```bash
# Deploy directly
render deploy

# Follow the prompts to create a new service
# Service type: Web Service
# Name: qiskit-backend (or your choice)
# Build command: (leave blank, uses render.yaml)
# Start command: (leave blank, uses render.yaml)
```

### Option B: Create Service First, Then Deploy

```bash
# Create the service
render services create web \
  --name qiskit-backend \
  --runtime python \
  --build-command "pip install -r requirements.txt" \
  --start-command "gunicorn server:app"

# Then deploy
render deploy
```

---

## Step 4: Monitor Deployment

```bash
# Watch logs in real-time
render logs -f

# Check deployment status
render services list
```

You'll see output like:
```
🚀 Deploying qiskit-backend...
📦 Installing dependencies...
✅ Build complete
🌐 Service live at: https://qiskit-backend-xyz.onrender.com
```

---

## Step 5: Test Your Deployed Service

Replace `YOUR_URL` with your actual Render URL:

```bash
# Health check
curl https://YOUR_URL.onrender.com/health

# Create session
curl -X POST https://YOUR_URL.onrender.com/session/create \
  -H "Content-Type: application/json"

# Execute code
curl -X POST https://YOUR_URL.onrender.com/session/execute \
  -H "Content-Type: application/json" \
  -d '{"session_id": "YOUR_SESSION_ID", "line": "qc = QuantumCircuit(2)"}'
```

---

## Step 6: Update Your HTML Frontend

Copy your deployed URL and update your HTML visualizer:

```javascript
// In your HTML file
const SERVER_CONFIG = {
    production: 'https://qiskit-backend-xyz.onrender.com',  // ← YOUR URL HERE
    local: 'http://localhost:5000',
    
    getServerUrl() {
        const isLocal = 
            window.location.hostname === 'localhost' || 
            window.location.hostname === '127.0.0.1' ||
            window.location.protocol === 'file:';
        
        return isLocal ? this.local : this.production;
    }
};
```

---

## Troubleshooting

### Deployment fails with dependency errors

Check `requirements.txt` versions:
```bash
pip freeze | grep -E "(flask|qiskit|numpy)"
```

### Service keeps restarting

Check logs:
```bash
render logs
```

Common issues:
- Port binding (use `PORT` env var)
- Missing dependencies
- Python version mismatch

### First request is slow

Render free tier spins down after 15 min of inactivity.
First request after idle takes ~30 seconds to wake up.

Solutions:
- Upgrade to paid tier ($7/month - always on)
- Use a ping service to keep it alive
- Accept the delay (it's free!)

---

## Render Dashboard Alternative

If CLI doesn't work, use the dashboard:

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect GitHub (push this code to GitHub first)
4. Select your repository
5. Render auto-detects `render.yaml` configuration
6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)

---

## Environment Variables (Optional)

Set in Render dashboard or CLI:

```bash
# Via CLI
render env set DEBUG=False

# Via dashboard
Dashboard → Your Service → Environment → Add Variable
```

Useful variables:
- `DEBUG` - Enable debug mode (default: False)
- `PYTHON_VERSION` - Python version (default: 3.11.0)

---

## Updating Your Service

After making changes:

```bash
# Commit changes
git add .
git commit -m "Update: description of changes"

# Deploy update
render deploy
```

Render will automatically rebuild and redeploy.

---

## Cost Estimate

**Free Tier:**
- 750 hours/month
- 512 MB RAM
- Spins down after 15 min idle
- Perfect for personal projects!

**Starter Tier ($7/month):**
- Always on
- 512 MB RAM
- No spin-down
- Better for production use

---

## Quick Commands Reference

```bash
# Deploy
render deploy

# View logs
render logs

# List services
render services list

# Delete service
render services delete qiskit-backend

# Check status
render services get qiskit-backend
```

---

## Success Checklist

✅ Local server runs without errors  
✅ Test script passes all tests  
✅ Git repository initialized  
✅ Deployed to Render successfully  
✅ Health check returns 200 OK  
✅ Can create session via API  
✅ Can execute Qiskit code  
✅ Frontend updated with production URL  

---

## Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Qiskit Docs**: https://qiskit.org/documentation

---

**You're ready to deploy! 🚀**

Run: `render deploy`
