from qiskit import QuantumCircuit
qc = QuantumCircuit(3)
qc.h(0)
qc.x(2)
qc.y(1)
qc.measure_all()
