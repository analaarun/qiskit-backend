#!/usr/bin/env python3
"""
Simple test to verify the server works locally before deploying
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_server():
    print("🧪 Testing Qiskit Backend Server")
    print("=" * 60)

    # Test 1: Health check
    print("\n1️⃣  Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("   ✅ PASS\n")
    except Exception as e:
        print(f"   ❌ FAIL: {e}\n")
        print("   Make sure server is running: python server.py")
        return

    # Test 2: Create session
    print("2️⃣  Create Session...")
    try:
        response = requests.post(f"{BASE_URL}/session/create")
        data = response.json()
        session_id = data['session_id']
        print(f"   Session ID: {session_id}")
        print(f"   ✅ PASS\n")
    except Exception as e:
        print(f"   ❌ FAIL: {e}\n")
        return

    # Test 3: Execute - Create circuit
    print("3️⃣  Execute: qc = QuantumCircuit(2)")
    try:
        response = requests.post(f"{BASE_URL}/session/execute", json={
            "session_id": session_id,
            "line": "qc = QuantumCircuit(2)"
        })
        data = response.json()
        print(f"   Success: {data['success']}")
        print(f"   Has circuit: {data.get('has_circuit', False)}")
        print(f"   Num qubits: {data.get('num_qubits', 'N/A')}")
        assert data['success'] == True
        print("   ✅ PASS\n")
    except Exception as e:
        print(f"   ❌ FAIL: {e}\n")
        return

    # Test 4: Execute - Add H gate
    print("4️⃣  Execute: qc.h(0)")
    try:
        response = requests.post(f"{BASE_URL}/session/execute", json={
            "session_id": session_id,
            "line": "qc.h(0)"
        })
        data = response.json()
        print(f"   Success: {data['success']}")
        print(f"   Gate count: {data.get('gate_count', 'N/A')}")
        print(f"   Bloch vector q0: x={data['bloch_vectors'][0]['x']:.3f}, "
              f"y={data['bloch_vectors'][0]['y']:.3f}, "
              f"z={data['bloch_vectors'][0]['z']:.3f}")
        assert data['success'] == True
        assert data['gate_count'] == 1
        print("   ✅ PASS\n")
    except Exception as e:
        print(f"   ❌ FAIL: {e}\n")
        return

    # Test 5: Execute - Add CNOT gate (create Bell state)
    print("5️⃣  Execute: qc.cx(0, 1) - Creating Bell State")
    try:
        response = requests.post(f"{BASE_URL}/session/execute", json={
            "session_id": session_id,
            "line": "qc.cx(0, 1)"
        })
        data = response.json()
        print(f"   Success: {data['success']}")
        print(f"   Gate count: {data.get('gate_count', 'N/A')}")
        print(f"   Probabilities: {data.get('probabilities', {})}")

        # Check Bell state: should have equal probability for |00⟩ and |11⟩
        probs = data.get('probabilities', {})
        assert abs(probs.get('00', 0) - 0.5) < 0.01, "Expected P(00) ≈ 0.5"
        assert abs(probs.get('11', 0) - 0.5) < 0.01, "Expected P(11) ≈ 0.5"
        assert probs.get('01', 0) < 0.01, "Expected P(01) ≈ 0"
        assert probs.get('10', 0) < 0.01, "Expected P(10) ≈ 0"

        print("   🎉 Bell state created correctly!")
        print("   ✅ PASS\n")
    except Exception as e:
        print(f"   ❌ FAIL: {e}\n")
        return

    # Test 6: Get state without execution
    print("6️⃣  Get Current State...")
    try:
        response = requests.post(f"{BASE_URL}/session/state", json={
            "session_id": session_id
        })
        data = response.json()
        print(f"   Success: {data['success']}")
        print(f"   Executed lines: {data.get('executed_lines', 'N/A')}")
        assert data['success'] == True
        print("   ✅ PASS\n")
    except Exception as e:
        print(f"   ❌ FAIL: {e}\n")
        return

    # Test 7: Delete session
    print("7️⃣  Delete Session...")
    try:
        response = requests.post(f"{BASE_URL}/session/delete", json={
            "session_id": session_id
        })
        data = response.json()
        print(f"   Success: {data['success']}")
        assert data['success'] == True
        print("   ✅ PASS\n")
    except Exception as e:
        print(f"   ❌ FAIL: {e}\n")
        return

    print("=" * 60)
    print("✅ ALL TESTS PASSED! Server is working correctly.")
    print("=" * 60)
    print("\n🚀 Ready to deploy to Render!")
    print("   Run: render deploy")

if __name__ == "__main__":
    test_server()
