import cudaq
import matplotlib.pyplot as plt
from collections import Counter

# Quantum kernel for GHZ state
@cudaq.kernel
def ghz(qubit_count: int):
    q = cudaq.qvector(qubit_count)
    h(q[0])
    for i in range(1, qubit_count):
        cx(q[0], q[i])
    mz(q)

# Sample the circuit using a specified target
def sample_ghz_state(qubit_count: int, target: str, backend_options: dict = None):
    print(f"\n🎯 Running GHZ({qubit_count}) on target: {target}")
    if backend_options:
        cudaq.set_target(target, **backend_options)
    else:
        cudaq.set_target(target)
    
    result = cudaq.sample(ghz, qubit_count, shots_count=1000)
    result.dump()
    return result

# Visualize the output using a bar chart
def plot_result(result, title):
    counts = Counter()
    for state in result:
        counts[str(state)] += result.count(state)

    plt.figure(figsize=(12, 6))
    plt.bar(counts.keys(), counts.values(), color='orange')
    plt.title(title)
    plt.xlabel("Measured State")
    plt.ylabel("Counts")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Main simulation
if __name__ == "__main__":
    qubit_count = 25

    # Use Multi-GPU (multi-QPU) target on NVIDIA backend
    result = sample_ghz_state(
        qubit_count=qubit_count,
        target="nvidia",
        backend_options={"option": "mqpu", "qpus": "1"}  # All values as strings
    )

    plot_result(result, f"GHZ({qubit_count}) State on Multi-GPU")
