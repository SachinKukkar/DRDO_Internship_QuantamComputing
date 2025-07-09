# import cudaq
# import matplotlib.pyplot as plt
# from collections import Counter


# @cudaq.kernel
# def ghz_state(qubit_count: int):
#     qubits = cudaq.qvector(qubit_count)
#     h(qubits[0])
#     for i in range(1, qubit_count):
#         cx(qubits[0], qubits[i])
#     mz(qubits)


# def sample_ghz_state(qubit_count: int, target: str):
#     print(f"\n🎯 Sampling GHZ({qubit_count}) on target: {target}")
#     cudaq.set_target(target)
#     result = cudaq.sample(ghz_state, qubit_count, shots_count=1000)
#     result.dump()  # Show raw results
#     return result


# def plot_results(result, title):
#     # Build histogram from SampleResult
#     counts = Counter()
#     for state in result:
#         counts[str(state)] += result.count(state)

#     # Plot
#     labels = list(counts.keys())
#     values = list(counts.values())

#     plt.figure(figsize=(10, 5))
#     plt.bar(labels, values, color="skyblue")
#     plt.xlabel("Measurement Outcome")
#     plt.ylabel("Counts")
#     plt.title(title)
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()


# if __name__ == "__main__":
#     cpu_qubits = 3
#     cpu_result = sample_ghz_state(cpu_qubits, "qpp-cpu")
#     plot_results(cpu_result, f"GHZ State on CPU ({cpu_qubits} qubits)")

#     if cudaq.num_available_gpus() > 0:
#         gpu_qubits = 5
#         gpu_result = sample_ghz_state(gpu_qubits, "nvidia")
#         plot_results(gpu_result, f"GHZ State on GPU ({gpu_qubits} qubits)")
#     else:
#         print("\n⚠️ No GPU available. Skipping GPU execution.")





