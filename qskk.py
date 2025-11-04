from qiskit import Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Run simulation
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend=backend, shots=1024)
result = job.result()

# Get measurement counts
counts = result.get_counts()
print("Measurement Results:", counts)

# Plot histogram
plot_histogram(counts)
plt.show()
