from qiskit import QuantumCircuit
from typing import Dict
from random import randint, shuffle


def xor_str(a: str, b: str) -> str:
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))


def create_2to1_map(mask: str) -> Dict[str, str]:
    """Generate a valid 2-to-1 function f(x) = f(x⊕s)"""
    n = len(mask)
    all_inputs = [format(i, f'0{n}b') for i in range(2**n)]
    shuffle(all_inputs)

    fmap = {}
    while all_inputs:
        x = all_inputs.pop()
        x_pair = xor_str(x, mask)
        if x_pair in all_inputs:
            all_inputs.remove(x_pair)
        y = format(randint(0, 2**n - 1), f'0{n}b')
        fmap[x] = y
        fmap[x_pair] = y
    return fmap


def build_simon_circuit(mask: str, fmap: Dict[str, str]) -> QuantumCircuit:
    n = len(mask)
    qc = QuantumCircuit(2 * n, n)

    # Step 1: Apply Hadamard to input qubits
    for i in range(n):
        qc.h(i)

def build_simon_circuit(mask: str, fmap: Dict[str, str]) -> QuantumCircuit:
    n = len(mask)
    qc = QuantumCircuit(2 * n, n)

    # Step 1: Apply Hadamard to input qubits
    for i in range(n):
        qc.h(i)

    # Step 2: Oracle (U_f)
    for x, fx in fmap.items():
        x_bits = [int(b) for b in x]
        fx_bits = [int(b) for b in fx]

        # Apply X gates to prepare input state |x⟩
        for i, bit in enumerate(x_bits):
            if bit == 0:
                qc.x(i)

        # Apply multi-controlled X gates to encode f(x) into output qubits
        for i, bit in enumerate(fx_bits):
            if bit == 1:
                qc.mcx(list(range(n)), n + i)  # Control on input, target output

        # Uncompute X gates
        for i, bit in enumerate(x_bits):
            if bit == 0:
                qc.x(i)

    # Step 3: Apply Hadamard again to input qubits
    for i in range(n):
        qc.h(i)

    # Step 4: Measure input qubits
    for i in range(n):
        qc.measure(i, i)

    return qc
    # Step 2: Placeholder for oracle
    qc.barrier()  # Indicates where oracle would be implemented

    # Step 3: Apply Hadamard again to input qubits
    for i in range(n):
        qc.h(i)

    # Step 4: Measure input qubits
    for i in range(n):
        qc.measure(i, i)

    return qc


def main():
    mask = input("Enter secret bitmask (e.g., 101): ").strip()
    if not all(c in "01" for c in mask):
        print("❌ Invalid input. Enter a binary string like '101'")
        return

    # Generate 2-to-1 mapping based on mask
    fmap = create_2to1_map(mask)
    print("\nGenerated 2-to-1 mapping (f(x) = f(x⊕s)):")
    for k in sorted(fmap):
        print(f"{k} -> {fmap[k]}")

    # Build and print the Simon's algorithm circuit
    circuit = build_simon_circuit(mask, fmap)
    print("\n🧠 Simon's Algorithm Quantum Circuit:")
    print(circuit.draw())  # ASCII circuit in terminal


if __name__ == "__main__":
    main()

