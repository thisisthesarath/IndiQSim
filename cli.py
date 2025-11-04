from circuit import QuantumCircuit
from gates import H, X, Y, Z
from utils.visualizer import plot_amplitudes
from utils.measurement import measure
from utils.circuit_visualizer import draw_circuit

def get_gate_choice():
    print("\nAvailable Gates:")
    print("1. Hadamard (H)")
    print("2. Pauli-X (X)")
    print("3. Pauli-Z (Z)")
    print("4. Pauli-Y (Y)")
    print("5. CNOT (CX)")
    print("6. Finish circuit")
    return input("Enter your choice (1-6): ").strip()

def main():
    print("=== IndiQSim Quantum CLI Simulator ===")
    num_qubits = int(input("Enter number of qubits: ").strip())
    qc = QuantumCircuit(num_qubits)
    gate_sequence = []  # This will be passed to draw_circuit

    while True:
        choice = get_gate_choice()

        if choice == '1':
            q = int(input("Apply H to which qubit? (0-indexed): "))
            qc.apply_gate(H, q)
            gate_sequence.append({"gate": "H", "target": q})
            print(f"Applied H to qubit {q}.")

        elif choice == '2':
            q = int(input("Apply X to which qubit? (0-indexed): "))
            qc.apply_gate(X, q)
            gate_sequence.append({"gate": "X", "target": q})
            print(f"Applied X to qubit {q}.")

        elif choice == '3':
            q = int(input("Apply Z to which qubit? (0-indexed): "))
            qc.apply_gate(Z, q)
            gate_sequence.append({"gate": "Z", "target": q})
            print(f"Applied Z to qubit {q}.")

        elif choice == '4':
            q = int(input("Apply Y to which qubit? (0-indexed): "))
            qc.apply_gate(Y, q)
            gate_sequence.append({"gate": "Y", "target": q})
            print(f"Applied Y to qubit {q}.")

        elif choice == '5':
            ctrl = int(input("Control qubit index: "))
            tgt = int(input("Target qubit index: "))
            qc.apply_cx(ctrl, tgt)
            gate_sequence.append({"gate": "CX", "control": ctrl, "target": tgt})
            print(f"Applied CX with control={ctrl}, target={tgt}.")

        elif choice == '6':
            break

        else:
            print("Invalid choice. Please enter 1–6.")

    # Final state vector
    print("\nFinal State Vector:")
    print(qc.state)

    # Measurement
    counts = measure(qc.state, shots=1024)
    print("\nMeasurement Counts:")
    print(counts)

    # Probability bar plot
    plot_amplitudes(qc.state)

    # Draw circuit
    draw_circuit(num_qubits, gate_sequence)

if __name__ == "__main__":
    main()
