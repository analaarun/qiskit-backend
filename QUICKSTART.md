# Quick Start Guide

Get your Qiskit backend running in 5 minutes!

---

## 📋 What You'll Need

- Python 3.9+ installed
- Render CLI authenticated ✅ (you've done this!)
- 10 minutes

---

## 🚀 Steps

### 1. Test Locally (2 minutes)

```bash
# Navigate to this directory
cd /Users/aanala/Desktop/ArunZone/Quantum/qiskit-backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python server.py
```

You should see:
```
============================================================
🚀 Qiskit Step Visualizer Backend Server
============================================================
   Port: 5000
   CORS: Enabled (all origins)
============================================================

 * Running on http://0.0.0.0:5000
```

**Leave this running!** Open a new terminal for the next step.

---

### 2. Test the Server (1 minute)

In a **new terminal**:

```bash
cd /Users/aanala/Desktop/ArunZone/Quantum/qiskit-backend

# Run the test
python test_simple.py
```

You should see:
```
🧪 Testing Qiskit Backend Server
============================================================

1️⃣  Health Check...
   Status: 200
   ✅ PASS

2️⃣  Create Session...
   Session ID: abc-123...
   ✅ PASS

3️⃣  Execute: qc = QuantumCircuit(2)
   ✅ PASS

4️⃣  Execute: qc.h(0)
   ✅ PASS

5️⃣  Execute: qc.cx(0, 1) - Creating Bell State
   🎉 Bell state created correctly!
   ✅ PASS

✅ ALL TESTS PASSED! Server is working correctly.
🚀 Ready to deploy to Render!
```

If all tests pass, you're ready to deploy! 🎉

---

### 3. Deploy to Render (5 minutes)

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Qiskit backend"

# Deploy to Render
render deploy
```

Follow the prompts:
- Service type: **Web Service**
- Name: **qiskit-backend** (or your choice)
- Build command: (leave blank)
- Start command: (leave blank)

Render will:
1. Upload your code
2. Install dependencies (~3 minutes)
3. Start your server
4. Give you a URL!

Your URL will look like:
```
https://qiskit-backend-xyz.onrender.com
```

**Copy this URL!** You'll need it for your HTML app.

---

### 4. Test Your Deployed Service (1 minute)

Replace `YOUR_URL` with your actual Render URL:

```bash
# Health check
curl https://YOUR_URL.onrender.com/health

# Should return:
# {"status": "healthy", "active_sessions": 0, ...}
```

If you see a healthy response, **you're live!** 🎉

---

## 🔗 Connect to Your HTML App

Update your HTML visualizer file:

```javascript
// Find this section in your HTML file
const SERVER_CONFIG = {
    production: 'https://qiskit-backend-xyz.onrender.com',  // ← Paste your URL here
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

Now your HTML app will:
- Use **local server** when developing (file://)
- Use **Render server** when deployed online

---

## ✅ Success Checklist

- ✅ Local server runs without errors
- ✅ All tests pass
- ✅ Deployed to Render
- ✅ Health check works
- ✅ HTML updated with production URL

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

```bash
pip install -r requirements.txt
```

### "Address already in use" (Port 5000 busy)

```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
PORT=8000 python server.py
```

### Render deployment fails

```bash
# Check logs
render logs

# Common issues:
# - requirements.txt missing a package
# - Python version mismatch
# - Syntax error in server.py
```

### First request to Render is slow (~30 seconds)

This is normal! Render's free tier spins down after 15 min of inactivity.
Subsequent requests are fast.

---

## 📊 Monitor Your Service

```bash
# View real-time logs
render logs -f

# List all services
render services list

# Get service info
render services get qiskit-backend
```

Or use the dashboard: https://dashboard.render.com

---

## 💰 Cost

**Free Tier (what you're using):**
- 750 hours/month
- Spins down after 15 min idle
- Perfect for development!

**Paid Tier ($7/month):**
- Always on
- No spin-down delay
- Better for production

---

## 🎉 You're Done!

Your Qiskit backend is now:
- ✅ Running locally for development
- ✅ Deployed to cloud for production
- ✅ Accessible from your HTML app

Test it by opening your HTML visualizer and toggling **"Use Python Backend"**!

---

## 📚 Next Steps

- Read [DEPLOY.md](DEPLOY.md) for advanced deployment options
- Read [README.md](README.md) for full API documentation
- Customize `server.py` to add features
- Deploy your HTML app to GitHub Pages / Netlify

---

## 🆘 Need Help?

- Check [DEPLOY.md](DEPLOY.md) troubleshooting section
- View logs: `render logs`
- Render docs: https://render.com/docs
- Qiskit docs: https://qiskit.org/documentation

---

**Questions? The files are well-commented - check `server.py` for details!**
