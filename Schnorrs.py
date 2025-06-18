from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
import numpy as np
import matplotlib.pyplot as plt


def discrete_log_example():
    """
    Simulate the structure of Schnorr's algorithm using QPE approach
    for solving a^x ≡ b (mod p) where p is a prime, and a, b are integers.
    """
    # Parameters (Toy values for demo)
    p = 7
    a = 3
    b = 5

    print(f"🔐 Solving for x in {a}^x ≡ {b} (mod {p})")

    # Simulated: Try all x until a^x % p == b (classical brute-force)
    for x in range(1, p):
        if pow(a, x, p) == b:
            print(f"✅ Solution found classically: x = {x}")
            break

    # Now: Build illustrative QPE-like quantum circuit
    n_count = 3  # 3 qubits for phase estimation (mock)
    qc = QuantumCircuit(n_count + 1, n_count)

    # Step 1: Apply Hadamards to counting register
    qc.h(range(n_count))

    # Step 2: Initialize target to |1⟩ (modular identity)
    qc.x(n_count)

    # Step 3: Placeholder for modular exponentiation
    for i in range(n_count):
        qc.cx(n_count, i)  # Mock controlled-unitaries

    # Step 4: Inverse QFT
    qc.append(QFT(n_count, inverse=True, do_swaps=True).to_gate(label="QFT†"), range(n_count))

    # Step 5: Measure
    qc.measure(range(n_count), range(n_count))

    print("📊 Schnorr’s Algorithm (Illustrative QPE for Discrete Log):")
    print(qc.draw())
    return


discrete_log_example()
