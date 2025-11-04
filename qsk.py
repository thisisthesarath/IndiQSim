from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Step 1: Create a quantum circuit with 2 qubits and 2 classical bits
qc = QuantumCircuit(2, 2)

# Step 2: Apply quantum gates
qc.h(0)      # Hadamard on qubit 0
qc.x(1)      # Pauli-X on qubit 1
qc.y(0)      # Pauli-Y on qubit 0
qc.z(1)      # Pauli-Z on qubit 1
qc.cx(0, 1)  # CNOT: control=0, target=1

# Step 3: Measure both qubits into classical bits
qc.measure([0, 1], [0, 1])

# Step 4: Run simulation using Aer backend
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend=backend, shots=1024)
result = job.result()

# Step 5: Get measurement results
counts = result.get_counts()
print("Measurement Results:", counts)

# Step 6: Plot results
plot_histogram(counts)
plt.title("Measurement Outcome Histogram")
plt.show()
