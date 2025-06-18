from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_city
import matplotlib.pyplot as plt
import numpy as np

# Oracle for |11⟩ (flips the phase of |11⟩ state)
def oracle(circuit, n):
    circuit.cz(n-2, n-1)

# Grover diffusion operator
def diffuser(n):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
  # multi-controlled Toffoli
    qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))
    return qc

# Create the circuit
n = 2
grover = QuantumCircuit(n)

# Step 1: Superposition
grover.h(range(n))

# Step 2: Oracle
oracle(grover, n)

# Step 3: Diffusion
grover.append(diffuser(n), range(n))

# Simulate with Statevector
state = Statevector.from_instruction(grover)
probabilities = state.probabilities_dict()

# Show probability distribution
print("Probabilities:", probabilities)

# Optional: visualize the statevector
plot_state_city(state)
plt.show()
