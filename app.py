"""
Qiskit Step Visualizer Backend Server
Stateful session-based execution for line-by-line Qiskit code
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from io import StringIO
import numpy as np
import uuid
import os
from datetime import datetime

# Qiskit imports
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

app = Flask(__name__)

# Enable CORS for all origins (frontend can be anywhere)
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# In-memory session storage
# For production scaling, consider Redis or similar
sessions = {}

class QuantumSession:
    """
    Maintains state for a single quantum computing session.
    Works like Jupyter: each line execution persists in the namespace.
    """

    def __init__(self, session_id):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.last_activity = datetime.now()

        # Execution namespace (like Jupyter cell context)
        self.namespace = {
            '__builtins__': __builtins__,
            'QuantumCircuit': QuantumCircuit,
            'np': np,
            'print': print
        }

        self.executed_lines = []
        self.current_circuit = None
        self.circuit_name = None

        # Pre-import common modules
        self._initialize_namespace()

    def _initialize_namespace(self):
        """Pre-import commonly used Qiskit modules"""
        imports = [
            "from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister",
            "import numpy as np",
            "import math"
        ]

        for import_line in imports:
            try:
                exec(import_line, self.namespace)
            except Exception as e:
                print(f"Warning: Could not pre-import: {import_line} - {e}")

    def execute_line(self, line_code):
        """
        Execute a single line of code in this session's namespace.
        Returns execution result with success status and any output/errors.
        """
        self.last_activity = datetime.now()

        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = StringIO()
        stderr_capture = StringIO()
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture

        try:
            # Compile and execute the code
            # Use compile() to properly handle multi-line blocks (with, if, for, while)
            compiled_code = compile(line_code, '<string>', 'exec')
            exec(compiled_code, self.namespace)

            # Update reference to quantum circuit if it exists
            self._update_circuit_reference()

            # Get captured output
            output = stdout_capture.getvalue()
            errors = stderr_capture.getvalue()

            # Track executed lines
            self.executed_lines.append({
                'line': line_code,
                'timestamp': datetime.now().isoformat()
            })

            return {
                'success': True,
                'output': output,
                'errors': errors if errors else None,
                'line_number': len(self.executed_lines)
            }

        except Exception as e:
            import traceback
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__,
                'traceback': traceback.format_exc()
            }
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def _update_circuit_reference(self):
        """Find and store reference to the quantum circuit in namespace"""
        for var_name, var_value in self.namespace.items():
            if isinstance(var_value, QuantumCircuit):
                self.current_circuit = var_value
                self.circuit_name = var_name
                break

    def get_quantum_state(self):
        """
        Extract current quantum state from the circuit.
        Returns statevector, Bloch vectors, probabilities, and circuit info.
        """
        if self.current_circuit is None:
            return {
                'has_circuit': False,
                'message': 'No quantum circuit created yet'
            }

        circuit = self.current_circuit
        num_qubits = circuit.num_qubits

        # Create copy for simulation (remove measurements)
        sim_circuit = circuit.copy()
        sim_circuit.remove_final_measurements(inplace=False)

        # Get statevector using Aer simulator
        simulator = AerSimulator(method='statevector')

        if len(sim_circuit.data) == 0:
            # Initial state |000...0⟩
            state_vector = np.zeros(2**num_qubits, dtype=complex)
            state_vector[0] = 1.0
        else:
            sim_circuit.save_statevector()
            result = simulator.run(sim_circuit).result()
            state_vector = result.get_statevector().data

        # Calculate Bloch vectors for each qubit
        bloch_vectors = []
        for q in range(num_qubits):
            bloch_vectors.append(self._calculate_bloch_vector(state_vector, num_qubits, q))

        # Calculate measurement probabilities for each basis state
        probabilities = {}
        for i in range(2**num_qubits):
            prob = float(np.abs(state_vector[i])**2)
            if prob > 1e-10:  # Only include non-zero probabilities
                basis_label = format(i, f'0{num_qubits}b')
                probabilities[basis_label] = prob

        # Format statevector for JSON serialization
        statevector_json = [
            {'re': float(np.real(amp)), 'im': float(np.imag(amp))}
            for amp in state_vector
        ]

        # Extract circuit operations for visualization
        operations = []
        for instruction in circuit.data:
            gate_info = {
                'gate': instruction.operation.name,
                'qubits': [circuit.find_bit(q).index for q in instruction.qubits],
            }
            # Include parameters if gate has them (e.g., rotation angles)
            if instruction.operation.params:
                gate_info['params'] = [float(p) for p in instruction.operation.params]
            operations.append(gate_info)

        return {
            'has_circuit': True,
            'num_qubits': num_qubits,
            'circuit_name': self.circuit_name,
            'statevector': statevector_json,
            'bloch_vectors': bloch_vectors,
            'probabilities': probabilities,
            'circuit_depth': circuit.depth(),
            'gate_count': len(circuit.data),
            'operations': operations
        }

    def _calculate_bloch_vector(self, statevector, num_qubits, qubit_index):
        """
        Calculate Bloch sphere coordinates for a specific qubit.
        Returns x, y, z components and vector length.
        Length < 1 indicates entanglement with other qubits.
        """
        dim = 2 ** num_qubits

        # Calculate reduced density matrix elements
        r00 = 0  # |0⟩⟨0|
        r01 = 0  # |0⟩⟨1|
        r11 = 0  # |1⟩⟨1|

        for i in range(dim):
            # Skip states where this qubit is |1⟩
            if (i >> qubit_index) & 1:
                continue

            # Get corresponding |1⟩ state by flipping this qubit
            j = i | (1 << qubit_index)

            a = statevector[i]  # amplitude for |0⟩
            b = statevector[j]  # amplitude for |1⟩

            r00 += np.abs(a) ** 2
            r11 += np.abs(b) ** 2
            r01 += a * np.conj(b)

        # Convert to Bloch vector coordinates
        x = 2 * np.real(r01)
        y = -2 * np.imag(r01)
        z = r00 - r11

        length = np.sqrt(x**2 + y**2 + z**2)

        return {
            'x': float(x),
            'y': float(y),
            'z': float(z),
            'length': float(length)
        }


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Health check and service info"""
    return jsonify({
        'status': 'running',
        'service': 'Qiskit Step Visualizer Backend',
        'version': '1.0.0',
        'active_sessions': len(sessions),
        'endpoints': {
            'health': '/health',
            'create_session': '/session/create',
            'execute_line': '/session/execute',
            'get_state': '/session/state',
            'reset_session': '/session/reset',
            'delete_session': '/session/delete'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'active_sessions': len(sessions),
        'qiskit_version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/session/create', methods=['POST'])
def create_session():
    """
    Create a new quantum computing session.
    Returns a session_id to use for subsequent requests.
    """
    session_id = str(uuid.uuid4())
    sessions[session_id] = QuantumSession(session_id)

    print(f"✅ Session created: {session_id}")

    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': 'Session created successfully',
        'created_at': sessions[session_id].created_at.isoformat()
    })


@app.route('/session/execute', methods=['POST'])
def execute_line():
    """
    Execute a single line of code in an existing session.
    The line executes in the session's persistent namespace (Jupyter-like).
    """
    data = request.json
    session_id = data.get('session_id')
    line_code = data.get('line')

    # Validate session
    if not session_id or session_id not in sessions:
        return jsonify({
            'success': False,
            'error': 'Invalid or expired session. Please create a new session.'
        }), 400

    if not line_code:
        return jsonify({
            'success': False,
            'error': 'No code provided'
        }), 400

    session = sessions[session_id]

    # Execute the line
    print(f"📝 Executing in session {session_id[:8]}...: {line_code[:50]}")
    result = session.execute_line(line_code)

    if not result['success']:
        print(f"❌ Execution error: {result['error']}")
        return jsonify(result)

    # Get current quantum state
    state_info = session.get_quantum_state()

    print(f"✓ Executed successfully. Circuit: {state_info.get('has_circuit')}")

    # Combine execution result with state information
    return jsonify({
        **result,
        **state_info
    })


@app.route('/session/state', methods=['POST'])
def get_session_state():
    """
    Get current quantum state without executing any code.
    Useful for refreshing the visualization.
    """
    data = request.json
    session_id = data.get('session_id')

    if not session_id or session_id not in sessions:
        return jsonify({
            'success': False,
            'error': 'Invalid or expired session'
        }), 400

    session = sessions[session_id]
    state_info = session.get_quantum_state()

    return jsonify({
        'success': True,
        **state_info,
        'executed_lines': len(session.executed_lines)
    })


@app.route('/session/reset', methods=['POST'])
def reset_session():
    """
    Reset a session to initial state.
    Clears all executed code and quantum circuit.
    """
    data = request.json
    session_id = data.get('session_id')

    if not session_id:
        return jsonify({
            'success': False,
            'error': 'No session_id provided'
        }), 400

    # Create fresh session with same ID
    sessions[session_id] = QuantumSession(session_id)

    print(f"🔄 Session reset: {session_id[:8]}...")

    return jsonify({
        'success': True,
        'message': 'Session reset successfully'
    })


@app.route('/session/delete', methods=['POST'])
def delete_session():
    """
    Delete a session and free its resources.
    """
    data = request.json
    session_id = data.get('session_id')

    if session_id and session_id in sessions:
        del sessions[session_id]
        print(f"🗑️  Session deleted: {session_id[:8]}...")

    return jsonify({
        'success': True,
        'message': 'Session deleted'
    })


@app.route('/sessions/cleanup', methods=['POST'])
def cleanup_sessions():
    """
    Clean up old inactive sessions (older than 1 hour).
    Can be called periodically to free memory.
    """
    from datetime import timedelta

    now = datetime.now()
    threshold = timedelta(hours=1)

    to_delete = []
    for session_id, session in sessions.items():
        if now - session.last_activity > threshold:
            to_delete.append(session_id)

    for session_id in to_delete:
        del sessions[session_id]

    return jsonify({
        'success': True,
        'cleaned': len(to_delete),
        'remaining': len(sessions)
    })


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/',
            '/health',
            '/session/create',
            '/session/execute',
            '/session/state',
            '/session/reset',
            '/session/delete'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': str(error)
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False') == 'True'

    print("=" * 60)
    print("🚀 Qiskit Step Visualizer Backend Server")
    print("=" * 60)
    print(f"   Port: {port}")
    print(f"   Debug: {debug}")
    print(f"   CORS: Enabled (all origins)")
    print("=" * 60)
    print()

    app.run(host='0.0.0.0', port=port, debug=debug)
