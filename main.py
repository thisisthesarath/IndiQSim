from gates import H, X  # Removed CX
from circuit import QuantumCircuit
from utils.visualizer import plot_amplitudes

# Create a 2-qubit quantum circuit
qc = QuantumCircuit(2)

# Apply Hadamard gate to qubit 0
qc.apply_gate(H, 0)

# Apply CNOT gate (control=0, target=1) to create entanglement
qc.apply_cx(0, 1)

# Print final state vector
print("Bell State Vector:")
print(qc.state)

# Plot the measurement probabilities
plot_amplitudes(qc.state)

# Measure results
counts = qc.measure(shots=1000)
print("Measurement Counts:")
print(counts)