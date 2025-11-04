# circuit.py
import numpy as np

class QuantumCircuit:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        # Initialize state |00…0>
        self.state = np.zeros((2**num_qubits, 1), dtype=complex)
        self.state[0, 0] = 1

    def apply_gate(self, gate_matrix, qubit_index):
        """Apply a single-qubit gate to qubit_index in an N-qubit system."""
        if not (0 <= qubit_index < self.num_qubits):
            raise IndexError(f"Qubit index {qubit_index} out of range.")
        # build full operator by tensoring I or gate
        ops = []
        for i in range(self.num_qubits):
            ops.append(gate_matrix if i == qubit_index else np.eye(2, dtype=complex))
        full_op = ops[0]
        for op in ops[1:]:
            full_op = np.kron(full_op, op)
        self.state = full_op.dot(self.state)

    def apply_cx(self, control, target):
        """Apply CNOT for any two distinct qubits in an N-qubit system."""
        if control == target:
            raise ValueError("Control and target must be different qubits.")
        if not (0 <= control < self.num_qubits) or not (0 <= target < self.num_qubits):
            raise IndexError("Control/target qubit index out of range.")

        # Build CNOT by summing projectors
        size = 2**self.num_qubits
        new_state = np.zeros_like(self.state)
        for basis_index in range(size):
            bits = [(basis_index >> i) & 1 for i in reversed(range(self.num_qubits))]
            if bits[self.num_qubits - 1 - control] == 0:
                # control=0 → unchanged
                new_state[basis_index, 0] += self.state[basis_index, 0]
            else:
                # control=1 → flip target bit
                bits_flipped = bits.copy()
                tgt_pos = self.num_qubits - 1 - target
                bits_flipped[tgt_pos] ^= 1
                new_index = sum(bit << (self.num_qubits - 1 - i)
                                for i, bit in enumerate(bits_flipped))
                new_state[new_index, 0] += self.state[basis_index, 0]
        self.state = new_state
