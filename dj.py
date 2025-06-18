from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


def deutsch_jozsa(n: int, is_balanced: bool) -> QuantumCircuit:
    """
    Deutsch-Jozsa algorithm circuit.
    :param n: Number of input qubits.
    :param is_balanced: Whether the function is balanced or constant.
    """
    qc = QuantumCircuit(n + 1, n)

    # Step 1: Initialize last qubit to |1⟩
    qc.x(n)
    qc.h(n)

    # Step 2: Apply Hadamard to input qubits
    qc.h(range(n))

    # Step 3: Oracle for f(x)
    if is_balanced:
        # Example balanced: flip last qubit based on x[0] XOR x[1] XOR ... x[n-1]
        for i in range(n):
            qc.cx(i, n)
    else:
        # Constant oracle (always returns 0 → does nothing)
        pass

    qc.barrier()

    # Step 4: Apply Hadamard to input qubits
    qc.h(range(n))

    # Step 5: Measure input qubits
    qc.measure(range(n), range(n))
    return qc


# CONFIGURATION
n_qubits = 3
is_balanced = True  # Toggle to False to simulate constant function

# Build and draw the circuit
dj_circuit = deutsch_jozsa(n_qubits, is_balanced)
print("🔎 Deutsch–Jozsa Circuit:")
print(dj_circuit.draw())

# Simulate using Statevector
sv = Statevector.from_label('0' * n_qubits + '1')
final_state = sv.evolve(dj_circuit.remove_final_measurements(inplace=False))

# Measurement result
counts = final_state.sample_counts(1024)
plot_histogram(counts)
plt.title("Deutsch–Jozsa Output Distribution")
plt.show()
