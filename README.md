# Qiskit Step Visualizer Backend

Stateful Python backend for executing Qiskit code line-by-line, like Jupyter Notebook.

## Features

- ✅ **Stateful Sessions** - Each line builds on previous execution (Jupyter-like)
- ✅ **Real Qiskit** - Uses actual Qiskit library, not simulation
- ✅ **Quantum State Extraction** - Returns statevector, Bloch vectors, probabilities
- ✅ **Session Management** - Create, execute, reset, delete sessions
- ✅ **CORS Enabled** - Works with any frontend (local or hosted)

## Quick Start

### Local Development

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run Server:**
```bash
python server.py
```

Server runs on `http://localhost:5000`

3. **Test it:**
```bash
curl http://localhost:5000/health
```

### Deploy to Render

1. **Initialize Git (if not already):**
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Create GitHub Repository:**
```bash
# Create repo on GitHub, then:
git remote add origin https://github.com/yourusername/qiskit-backend.git
git push -u origin main
```

3. **Deploy on Render:**

**Option A: Using Render CLI**
```bash
render deploy
```

**Option B: Using Dashboard**
- Go to https://dashboard.render.com
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Render auto-detects configuration from `render.yaml`
- Click "Create Web Service"

4. **Get Your URL:**
```
https://qiskit-backend-xyz.onrender.com
```

## API Endpoints

### `GET /` - Service Info
Returns service information and available endpoints.

### `GET /health` - Health Check
```json
{
  "status": "healthy",
  "active_sessions": 2,
  "qiskit_version": "1.0.0"
}
```

### `POST /session/create` - Create Session
Creates a new quantum computing session.

**Response:**
```json
{
  "success": true,
  "session_id": "abc-123-def-456",
  "message": "Session created successfully"
}
```

### `POST /session/execute` - Execute Line
Execute a single line of code in a session.

**Request:**
```json
{
  "session_id": "abc-123-def-456",
  "line": "qc.h(0)"
}
```

**Response:**
```json
{
  "success": true,
  "output": "",
  "has_circuit": true,
  "num_qubits": 2,
  "statevector": [
    {"re": 0.707, "im": 0.0},
    {"re": 0.707, "im": 0.0},
    {"re": 0.0, "im": 0.0},
    {"re": 0.0, "im": 0.0}
  ],
  "bloch_vectors": [
    {"x": 1.0, "y": 0.0, "z": 0.0, "length": 1.0},
    {"x": 0.0, "y": 0.0, "z": 1.0, "length": 1.0}
  ],
  "probabilities": {
    "00": 0.5,
    "01": 0.5
  },
  "gate_count": 1,
  "circuit_depth": 1
}
```

### `POST /session/state` - Get State
Get current quantum state without executing code.

**Request:**
```json
{
  "session_id": "abc-123-def-456"
}
```

### `POST /session/reset` - Reset Session
Clear all executed code and reset to initial state.

**Request:**
```json
{
  "session_id": "abc-123-def-456"
}
```

### `POST /session/delete` - Delete Session
Delete a session and free resources.

**Request:**
```json
{
  "session_id": "abc-123-def-456"
}
```

## Example Usage (JavaScript)

```javascript
// Create session
const response = await fetch('http://localhost:5000/session/create', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'}
});
const { session_id } = await response.json();

// Execute line 1
await fetch('http://localhost:5000/session/execute', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    session_id,
    line: 'qc = QuantumCircuit(2)'
  })
});

// Execute line 2 (builds on line 1)
await fetch('http://localhost:5000/session/execute', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    session_id,
    line: 'qc.h(0)'
  })
});

// Execute line 3 (builds on lines 1-2)
const result = await fetch('http://localhost:5000/session/execute', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    session_id,
    line: 'qc.cx(0, 1)'
  })
});

const data = await result.json();
console.log('Bell state created!', data.probabilities);
// Output: { "00": 0.5, "11": 0.5 }
```

## Architecture

```
Client (HTML/JS) → HTTP Requests → Flask Server
                                    ├─ Session Manager
                                    ├─ Code Executor
                                    └─ Qiskit Simulator
```

Each session maintains:
- **Persistent namespace** (like Jupyter cells)
- **Executed line history**
- **Current quantum circuit reference**
- **Last activity timestamp**

## Environment Variables

- `PORT` - Server port (default: 5000)
- `DEBUG` - Enable debug mode (default: False)

## Security Notes

- Sessions are stored in memory (use Redis for production scaling)
- No authentication implemented (add if deploying publicly)
- CORS is open to all origins (restrict in production if needed)
- Code execution is unrestricted (sandboxing recommended for public use)

## Troubleshooting

### Local server won't start
```bash
# Check if port 5000 is in use
lsof -ti:5000 | xargs kill -9

# Try different port
PORT=8000 python server.py
```

### Qiskit import errors
```bash
pip install --upgrade qiskit qiskit-aer
```

### Render deployment fails
- Check logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Verify Python version compatibility

## License

MIT

## Author

Created for Qiskit Step Visualizer project
