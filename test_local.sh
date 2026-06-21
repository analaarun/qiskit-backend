#!/bin/bash

# Test script for local development

echo "🧪 Testing Qiskit Backend Server"
echo "=================================="
echo ""

BASE_URL="http://localhost:5000"

# Check if server is running
echo "1. Health Check..."
curl -s $BASE_URL/health | python3 -m json.tool
echo ""
echo ""

# Create session
echo "2. Creating session..."
SESSION_RESPONSE=$(curl -s -X POST $BASE_URL/session/create -H "Content-Type: application/json")
echo $SESSION_RESPONSE | python3 -m json.tool
SESSION_ID=$(echo $SESSION_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['session_id'])")
echo ""
echo "Session ID: $SESSION_ID"
echo ""
echo ""

# Execute line 1: Create circuit
echo "3. Executing: qc = QuantumCircuit(2)"
curl -s -X POST $BASE_URL/session/execute \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"line\": \"qc = QuantumCircuit(2)\"}" \
  | python3 -m json.tool
echo ""
echo ""

# Execute line 2: Add H gate
echo "4. Executing: qc.h(0)"
curl -s -X POST $BASE_URL/session/execute \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"line\": \"qc.h(0)\"}" \
  | python3 -m json.tool
echo ""
echo ""

# Execute line 3: Add CNOT gate
echo "5. Executing: qc.cx(0, 1)"
curl -s -X POST $BASE_URL/session/execute \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"line\": \"qc.cx(0, 1)\"}" \
  | python3 -m json.tool
echo ""
echo ""

# Get current state
echo "6. Getting current state..."
curl -s -X POST $BASE_URL/session/state \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\"}" \
  | python3 -m json.tool
echo ""
echo ""

# Delete session
echo "7. Cleaning up session..."
curl -s -X POST $BASE_URL/session/delete \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\"}" \
  | python3 -m json.tool
echo ""
echo ""

echo "✅ Test complete!"
