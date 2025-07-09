import cudaq


# Define our kernel.
@cudaq.kernel
def kernel(qubit_count: int):
    # Allocate our qubits.
    qvector = cudaq.qvector(qubit_count)
    # Place the first qubit in the superposition state.
    h(qvector[0])
    # Loop through the allocated qubits and apply controlled-X,
    # or CNOT, operations between them.
    for qubit in range(qubit_count - 1):
        x.ctrl(qvector[qubit], qvector[qubit + 1])
    # Measure the qubits.
    mz(qvector)


qubit_count = 2
print(cudaq.draw(kernel, qubit_count))
results = cudaq.sample(kernel, qubit_count)
# Should see a roughly 50/50 distribution between the |00> and
# |11> states. Example: {00: 505  11: 495}
print("Measurement distribution:" + str(results))    

results = cudaq.sample(kernel, qubit_count, shots_count=10000)
print("Measurement distribution:" + str(results))


most_probable_result = results.most_probable()
probability = results.probability(most_probable_result)
print("Most probable result: " + most_probable_result)
print("Measured with probability " + str(probability), end='\n\n')





@cudaq.kernel
def kernel2(qubit_count: int):
    # Allocate our qubits.
    qvector = cudaq.qvector(qubit_count)
    # Place all qubits in a uniform superposition.
    h(qvector)
    # Measure the qubits.
    mz(qvector)


num_gpus = cudaq.num_available_gpus()
if num_gpus > 1:
    # Set the target to include multiple virtual QPUs.
    cudaq.set_target("nvidia", option="mqpu")
    # Asynchronous execution on multiple virtual QPUs, each simulated by an NVIDIA GPU.
    result_1 = cudaq.sample_async(kernel,
                                  qubit_count,
                                  shots_count=1000,
                                  qpu_id=0)
    result_2 = cudaq.sample_async(kernel2,
                                  qubit_count,
                                  shots_count=1000,
                                  qpu_id=1)
else:
    # Schedule for execution on the same virtual QPU.
    result_1 = cudaq.sample_async(kernel,
                                  qubit_count,
                                  shots_count=1000,
                                  qpu_id=0)
    result_2 = cudaq.sample_async(kernel2,
                                  qubit_count,
                                  shots_count=1000,
                                  qpu_id=0)

print("Measurement distribution for kernel:" + str(result_1.get()))
print("Measurement distribution for kernel2:" + str(result_2.get()))



import sys
import cudaq
import timeit

# Will time the execution of our sample call.
code_to_time = 'cudaq.sample(kernel, qubit_count, shots_count=1000000)'
qubit_count = int(sys.argv[1]) if 1 < len(sys.argv) else 25

# Execute on CPU backend.
cudaq.set_target('qpp-cpu')
print('CPU time')  # Example: 27.57462 s.
print(timeit.timeit(stmt=code_to_time, globals=globals(), number=1))

if cudaq.num_available_gpus() > 0:
    # Execute on GPU backend.
    cudaq.set_target('nvidia')
    print('GPU time')  # Example: 0.773286 s.
    print(timeit.timeit(stmt=code_to_time, globals=globals(), number=1))