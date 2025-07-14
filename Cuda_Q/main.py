import cudaq
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import numpy as np
import time
import platform
import psutil
import GPUtil
from collections import Counter
import threading

sns.set_context("notebook")
sns.set_style("darkgrid")

cpu_percent_history = []
gpu_load_history = []
gpu_mem_history = []
time_history = []
start_time = time.time()

@cudaq.kernel
def ghz(qubit_count: int):
    q = cudaq.qvector(qubit_count)
    h(q[0])
    for i in range(1, qubit_count):
        cx(q[0], q[i])
    mz(q)

fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("🚀 Real-Time CUDA-Q Quantum Benchmarking Dashboard", fontsize=16, weight='bold')

cpu_line, = axs[0, 0].plot([], [], label='CPU %', color='tab:blue')
gpu_line, = axs[0, 1].plot([], [], label='GPU Load %', color='tab:green')
mem_line, = axs[1, 0].plot([], [], label='GPU Mem %', color='tab:red')

for ax in [axs[0, 0], axs[0, 1], axs[1, 0]]:
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 100)
    ax.grid(True)
    ax.legend()

axs[0, 0].set_title("CPU Usage (%)")
axs[0, 1].set_title("GPU Load (%)")
axs[1, 0].set_title("GPU Memory Usage (%)")
histogram_ax = axs[1, 1]

def update(frame):
    elapsed = time.time() - start_time
    time_history.append(elapsed)

    cpu = psutil.cpu_percent()
    cpu_percent_history.append(cpu)
    cpu_line.set_data(time_history, cpu_percent_history)

    try:
        gpus = GPUtil.getGPUs()
        gpu_load = gpus[0].load * 100
        gpu_mem = (gpus[0].memoryUsed / gpus[0].memoryTotal) * 100
    except:
        gpu_load = 0
        gpu_mem = 0

    gpu_load_history.append(gpu_load)
    gpu_mem_history.append(gpu_mem)

    gpu_line.set_data(time_history, gpu_load_history)
    mem_line.set_data(time_history, gpu_mem_history)

    for ax in [axs[0, 0], axs[0, 1], axs[1, 0]]:
        ax.set_xlim(max(0, elapsed - 30), elapsed + 1)

    return cpu_line, gpu_line, mem_line

ani = animation.FuncAnimation(fig, update, interval=200)

def perform_heavy_gpu_sampling(qubit_count, batches=25):
    cudaq.set_target("nvidia")
    all_results = []
    print(f"\n🟢 Running GHZ({qubit_count}) for {batches} batches on GPU...")

    for i in range(batches):
        print(f"Batch {i+1}/{batches}...", end='\r')
        result = cudaq.sample(ghz, qubit_count, shots_count=10000)
        all_results.extend(result)

    counts = Counter()
    for state in all_results:
        counts[str(state)] += all_results.count(state)

    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    histogram_ax.clear()
    histogram_ax.bar(sorted_counts.keys(), sorted_counts.values(), color=sns.color_palette("deep"))
    histogram_ax.set_title(f"GHZ({qubit_count}) Result (GPU)")
    histogram_ax.set_xlabel("Bitstrings")
    histogram_ax.set_ylabel("Frequency")
    histogram_ax.tick_params(axis='x', rotation=90)

if __name__ == "__main__":
    print("🚀 DRDO CUDA-Q Benchmarking Dashboard")
    print(f"🧠 OS: {platform.system()} | CUDA-Q: {cudaq.__version__}")
    print(f"🎯 CUDA GPUs: {cudaq.num_available_gpus()} available\n")

    if cudaq.num_available_gpus() == 0:
        print("❌ No CUDA GPUs found by CUDA-Q. Aborting.")
    else:
        ghz_thread = threading.Thread(target=perform_heavy_gpu_sampling, args=(12,))
        ghz_thread.start()

        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        plt.show()

        ghz_thread.join()
        print("✅ Benchmarking Complete.")
