from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


def bernstein_vazirani(s: str) -> QuantumCircuit:
    """
    Bernstein-Vazirani algorithm to find hidden string s
    :param s: Secret binary string (e.g., '1101')
    """
    n = len(s)
    qc = QuantumCircuit(n + 1, n)

    # Initialize ancilla to |1⟩
    qc.x(n)
    qc.h(n)

    # Apply Hadamard to input qubits
    qc.h(range(n))

    # Oracle for f(x) = s · x (mod 2)
    for i, bit in enumerate(s):
        if bit == '1':
            qc.cx(i, n)

    # Apply Hadamard to input again
    qc.h(range(n))

    # Measure only input qubits
    qc.measure(range(n), range(n))
    return qc


# Run the circuit
secret = '1011'
bv_circuit = bernstein_vazirani(secret)

print("🔎 Bernstein-Vazirani Circuit:")
print(bv_circuit.draw())

# Simulate using Statevector
sv = Statevector.from_label('0' * (len(secret)) + '1')
final_state = sv.evolve(bv_circuit.remove_final_measurements(inplace=False))

# Plot measurement outcome
counts = final_state.sample_counts(1024)
plot_histogram(counts)
plt.title("Bernstein-Vazirani Output Distribution")
plt.show()
