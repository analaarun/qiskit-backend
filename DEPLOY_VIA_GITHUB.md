# Alternative: Deploy via GitHub (No CLI Required!)

If the Render CLI isn't working, use GitHub + Render Dashboard instead.

---

## 📋 Steps (10 minutes total)

### **Step 1: Push to GitHub** (3 minutes)

```bash
cd /Users/aanala/Desktop/ArunZone/Quantum/qiskit-backend

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Qiskit backend"

# Create repo on GitHub:
# Go to https://github.com/new
# Name: qiskit-backend
# Click "Create repository"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/qiskit-backend.git

# Push
git branch -M main
git push -u origin main
```

---

### **Step 2: Deploy on Render Dashboard** (5 minutes)

1. **Go to:** https://dashboard.render.com

2. **Click:** "New +" → "Web Service"

3. **Connect GitHub:**
   - Click "Connect GitHub"
   - Select your repository: `qiskit-backend`

4. **Configure Service:**
   - **Name:** `qiskit-backend` (or your choice)
   - **Runtime:** Python ✅ (auto-detected)
   - **Build Command:** (leave blank - uses render.yaml)
   - **Start Command:** (leave blank - uses render.yaml)

5. **Click:** "Create Web Service"

6. **Wait:** 5-10 minutes for deployment

7. **Copy URL:** 
   ```
   https://qiskit-backend-xyz.onrender.com
   ```

---

### **Step 3: Test Your Service**

```bash
# Replace with YOUR actual URL
curl https://qiskit-backend-xyz.onrender.com/health

# Should return:
{
  "status": "healthy",
  "active_sessions": 0,
  "qiskit_version": "1.0.0"
}
```

If you see this, **you're live!** 🎉

---

## 🎯 What You Get

Your deployed backend will be at:
```
https://qiskit-backend-[your-slug].onrender.com
```

**All endpoints available:**
- `GET  /health` - Health check
- `POST /session/create` - Create session
- `POST /session/execute` - Execute code
- `POST /session/state` - Get state
- `POST /session/reset` - Reset session
- `POST /session/delete` - Delete session

---

## 🔄 Future Updates

After initial deployment, updates are automatic:

```bash
# Make changes to server.py
# Then:
git add .
git commit -m "Updated: description"
git push

# Render auto-deploys! (5 minutes)
```

---

## 📊 Monitor Your Service

**Dashboard:**
https://dashboard.render.com

**View Logs:**
- Dashboard → Your Service → Logs
- Or CLI: `render logs`

**Check Status:**
- Dashboard → Your Service → Events

---

## 💰 Pricing

**Free Tier (what you're using):**
- 750 hours/month
- 512 MB RAM
- Spins down after 15 min idle
- Perfect for development!

**Note:** First request after idle takes ~30 seconds (spin-up time)

---

## ✅ Success Checklist

- ✅ Code pushed to GitHub
- ✅ Render service created
- ✅ Deployment succeeded (green checkmark)
- ✅ Health endpoint returns 200
- ✅ URL copied for HTML integration

---

## 🆘 Troubleshooting

### "Build failed"
- Check logs in Render dashboard
- Usually: missing dependency in requirements.txt

### "Service won't start"
- Check logs for Python errors
- Verify render.yaml is correct

### "Can't connect to GitHub"
- Make sure repo is public
- Or grant Render access to private repos

---

## 🎉 You're Done!

Your backend is now:
- ✅ Deployed to cloud
- ✅ Accessible from anywhere
- ✅ Auto-updates on git push

**Next:** Update your HTML with the production URL!
