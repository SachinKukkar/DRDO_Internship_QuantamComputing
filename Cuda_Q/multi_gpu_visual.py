import cudaq
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
import platform
import psutil
import GPUtil
import threading
from collections import Counter

# Set visual style
sns.set_context("notebook")
sns.set_style("darkgrid")

cpu_percent_history = []
gpu_load_history = []
gpu_mem_history = []
time_history = []

# Quantum kernel for GHZ state
@cudaq.kernel
def ghz(qubit_count: int):
    q = cudaq.qvector(qubit_count)
    h(q[0])
    for i in range(1, qubit_count):
        cx(q[0], q[i])
    mz(q)

# Function to sample GHZ state
def sample_ghz_state(qubit_count: int, target: str, backend_options: dict = None):
    if backend_options:
        cudaq.set_target(target, **backend_options)
    else:
        cudaq.set_target(target)

    start = time.time()
    result = cudaq.sample(ghz, qubit_count, shots_count=1000)
    end = time.time()
    return result, end - start

# Real-time system monitor during execution
def monitor_resources(duration=10):
    start_time = time.time()
    while time.time() - start_time < duration:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_percent_history.append(cpu_percent)

        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_load = gpus[0].load * 100
                gpu_mem = (gpus[0].memoryUsed / gpus[0].memoryTotal) * 100
            else:
                gpu_load = 0
                gpu_mem = 0
        except:
            gpu_load = 0
            gpu_mem = 0

        gpu_load_history.append(gpu_load)
        gpu_mem_history.append(gpu_mem)
        time_history.append(time.time() - start_time)

# Plot dynamic CPU and GPU resource usage
def plot_resource_usage():
    plt.figure(figsize=(12, 6))
    plt.plot(time_history, cpu_percent_history, label="CPU Usage %", color="tab:blue")
    plt.plot(time_history, gpu_load_history, label="GPU Load %", color="tab:green")
    plt.plot(time_history, gpu_mem_history, label="GPU Memory %", color="tab:red")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.title("Real-Time Resource Utilization")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("real_time_resource_usage.png", dpi=300)
    plt.show(block=False)
    plt.pause(0.1)

# Plot measurement results
def plot_result(result, title, filename=None):
    counts = Counter()
    for state in result:
        counts[str(state)] += result.count(state)
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    plt.figure(figsize=(14, 6))
    bars = plt.bar(sorted_counts.keys(), sorted_counts.values(), color=sns.color_palette("deep"))
    plt.title(title, fontsize=16, weight='bold')
    plt.xlabel("Quantum Measurement Outcomes")
    plt.ylabel("Frequency (out of 1000 shots)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 5, int(yval), ha='center', fontsize=8)
    if filename:
        plt.savefig(filename, dpi=300)
    plt.show(block=False)
    plt.pause(0.1)

# Benchmark and compare CPU vs GPU
def benchmark(qubit_count):
    benchmarks = []

    print("\n🔵 Sampling using CPU (qpp-cpu)...")
    result_cpu, time_cpu = sample_ghz_state(qubit_count, target="qpp-cpu")
    plot_result(result_cpu, f"GHZ({qubit_count}) on CPU", filename="ghz_cpu.png")
    benchmarks.append(('CPU', time_cpu))

    if cudaq.num_available_gpus() > 0:
        print("\n🟢 Sampling using GPU (nvidia)...")
        monitor_resources_thread = threading.Thread(target=monitor_resources, args=(5,))
        monitor_resources_thread.start()
        result_gpu, time_gpu = sample_ghz_state(qubit_count, target="nvidia")
        monitor_resources_thread.join()
        plot_result(result_gpu, f"GHZ({qubit_count}) on GPU", filename="ghz_gpu.png")
        benchmarks.append(('GPU', time_gpu))

        print("\n🟣 Sampling using Multi-GPU (mqpu)...")
        qpu_count = cudaq.num_available_gpus()
        result_mgpu, time_mgpu = sample_ghz_state(
            qubit_count, target="nvidia", backend_options={"option": "mqpu", "qpus": str(qpu_count)}
        )
        plot_result(result_mgpu, f"GHZ({qubit_count}) on MQPU ({qpu_count} QPUs)", filename="ghz_mgpu.png")
        benchmarks.append((f"MQPU x{qpu_count}", time_mgpu))
    else:
        print("❌ No GPU available. Skipping GPU and MQPU benchmarks.")

    return benchmarks

# Plot benchmark comparison
def plot_benchmarks(benchmarks):
    labels, times = zip(*benchmarks)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=labels, y=times, palette="coolwarm")
    plt.title("⏱️ Execution Time Comparison", fontsize=15, weight='bold')
    plt.ylabel("Execution Time (seconds)")
    plt.xlabel("Execution Target")
    for i, t in enumerate(times):
        plt.text(i, t + 0.01, f"{t:.3f}s", ha='center', fontsize=10)
    plt.tight_layout()
    plt.savefig("execution_comparison.png", dpi=300)
    plt.show(block=False)
    plt.pause(0.1)

# Main execution
if __name__ == "__main__":
    print("🚀 DRDO Quantum Benchmarking Suite — CUDA-Q")
    print(f"🧬 System: {platform.system()} {platform.release()}")
    print(f"🧪 Python: {platform.python_version()} | CUDA-Q: {cudaq.__version__}\n")

    qubit_count = 20  # Recommended for GPU — increase if multi-GPU available
    benchmarks = benchmark(qubit_count)
    plot_benchmarks(benchmarks)
    plot_resource_usage()

    input("\n✅ All plots displayed. Press Enter to close everything and exit...")
