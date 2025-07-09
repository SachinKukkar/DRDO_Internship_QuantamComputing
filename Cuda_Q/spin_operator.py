import cudaq
from cudaq import spin

operator = spin.z(0)
print(operator)  # prints: [1+0j] Z


@cudaq.kernel
def kernel():
    qubit = cudaq.qubit()
    h(qubit)

# result = cudaq.observe(kernel, operator)
# print(result.expectation())  # prints: 0.0   

result = cudaq.observe(kernel, operator, shots_count=1000)
print(result.expectation())  # prints non-zero value