from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt


def grover_oracle(qc, target):
    """Oracle to flip the sign of the target state"""
    n = len(target)
    for i, bit in enumerate(target):
        if bit == '0':
            qc.x(i)
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    for i, bit in enumerate(target):
        if bit == '0':
            qc.x(i)


def diffuser(qc, n):
    """Inversion about the mean (diffuser)"""
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))


def grover_algorithm(n, target_bin):
    """Grover circuit for n-qubit with one marked state"""
    qc = QuantumCircuit(n, n)

    # Step 1: Initialize with Hadamard
    qc.h(range(n))

    # Step 2: Oracle
    grover_oracle(qc, target_bin)
    qc.barrier()

    # Step 3: Diffuser
    diffuser(qc, n)
    qc.barrier()

    # Step 4: Measure
    qc.measure(range(n), range(n))
    return qc


# Parameters
n = 3
target_state = '101'

# Build circuit
grover_circuit = grover_algorithm(n, target_state)
print("\n🔍 Grover's Circuit:")
print(grover_circuit.draw())

# Simulate using Statevector (for visualization)
init_sv = Statevector.from_label('0'*n)
final_sv = init_sv.evolve(grover_circuit.remove_final_measurements(inplace=False))

# Plot Bloch vectors and measurement outcomes
plot_bloch_multivector(final_sv)
plt.show()

# Show output probabilities
counts = final_sv.sample_counts(1000)
plot_histogram(counts)
plt.show()
