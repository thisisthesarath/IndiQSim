import tkinter as tk
from tkinter import messagebox, ttk
from circuit import QuantumCircuit
from gates import H, X, Y, Z
from utils.visualizer import plot_amplitudes
from utils.measurement import measure
from utils.circuit_visualizer import draw_circuit

class QuantumGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("IndiQSim Quantum Simulator")
        self.master.configure(bg="#1e1e2f")
        self.master.geometry("700x500")
        self.gate_sequence = []
        self.qc = None

        self.setup_style()
        self.init_qubit_selector()

    def setup_style(self):
        style = ttk.Style()
        style.configure("TButton",
                        font=("Segoe UI", 12),
                        padding=6)
        style.configure("TLabel",
                        background="#1e1e2f",
                        foreground="white",
                        font=("Segoe UI", 12))

    def init_qubit_selector(self):
        self.selector_frame = ttk.Frame(self.master)
        self.selector_frame.pack(pady=50)

        label = ttk.Label(self.selector_frame, text="Select number of qubits (1-5):")
        label.pack(pady=10)

        self.qubit_var = tk.IntVar(value=2)
        self.qubit_dropdown = ttk.Combobox(self.selector_frame, textvariable=self.qubit_var, values=list(range(1, 6)), font=("Segoe UI", 12), state="readonly")
        self.qubit_dropdown.pack(pady=10)

        start_btn = ttk.Button(self.selector_frame, text="Start Simulation", command=self.start_simulation)
        start_btn.pack(pady=10)

    def start_simulation(self):
        num_qubits = self.qubit_var.get()
        self.qc = QuantumCircuit(num_qubits)
        self.num_qubits = num_qubits

        self.selector_frame.destroy()
        self.create_main_ui()

    def create_main_ui(self):
        self.frame = ttk.Frame(self.master)
        self.frame.pack(pady=20)

        label = ttk.Label(self.frame, text=f"Quantum Circuit Simulator ({self.num_qubits} Qubits)", font=("Segoe UI", 14, "bold"))
        label.pack(pady=10)

        gate_frame = ttk.Frame(self.frame)
        gate_frame.pack(pady=10)

        ttk.Button(gate_frame, text="Hadamard (H)", command=self.apply_h).pack(side=tk.LEFT, padx=5)
        ttk.Button(gate_frame, text="Pauli-X (X)", command=self.apply_x).pack(side=tk.LEFT, padx=5)
        ttk.Button(gate_frame, text="Pauli-Y (Y)", command=self.apply_y).pack(side=tk.LEFT, padx=5)
        ttk.Button(gate_frame, text="Pauli-Z (Z)", command=self.apply_z).pack(side=tk.LEFT, padx=5)
        ttk.Button(gate_frame, text="CNOT (CX)", command=self.apply_cx).pack(side=tk.LEFT, padx=5)

        control_frame = ttk.Frame(self.frame)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Target Qubit:").pack(side=tk.LEFT)
        self.target_entry = ttk.Entry(control_frame, width=3)
        self.target_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Control Qubit (for CX):").pack(side=tk.LEFT)
        self.control_entry = ttk.Entry(control_frame, width=3)
        self.control_entry.pack(side=tk.LEFT, padx=5)

        action_frame = ttk.Frame(self.frame)
        action_frame.pack(pady=20)

        ttk.Button(action_frame, text="Measure", command=self.measure).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="Draw Circuit", command=self.draw_circuit).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=10)

    def apply_gate(self, gate_func, gate_name):
        try:
            q = int(self.target_entry.get())
            if 0 <= q < self.num_qubits:
                self.qc.apply_gate(gate_func, q)
                self.gate_sequence.append({"gate": gate_name, "target": q})
                messagebox.showinfo("Gate Applied", f"{gate_name} applied to qubit {q}.")
            else:
                messagebox.showerror("Error", "Invalid target qubit index.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid target qubit index.")

    def apply_h(self):
        self.apply_gate(H, "H")

    def apply_x(self):
        self.apply_gate(X, "X")

    def apply_y(self):
        self.apply_gate(Y, "Y")

    def apply_z(self):
        self.apply_gate(Z, "Z")

    def apply_cx(self):
        try:
            ctrl = int(self.control_entry.get())
            tgt = int(self.target_entry.get())
            if 0 <= ctrl < self.num_qubits and 0 <= tgt < self.num_qubits and ctrl != tgt:
                self.qc.apply_cx(ctrl, tgt)
                self.gate_sequence.append({"gate": "CX", "control": ctrl, "target": tgt})
                messagebox.showinfo("Gate Applied", f"CX applied with control={ctrl}, target={tgt}.")
            else:
                messagebox.showerror("Error", "Invalid control or target index, or they are equal.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid qubit indices.")

    def measure(self):
        counts = measure(self.qc.state, shots=1024)
        plot_amplitudes(self.qc.state)
        messagebox.showinfo("Measurement", str(counts))

    def draw_circuit(self):
        draw_circuit(self.num_qubits, self.gate_sequence)
        messagebox.showinfo("Circuit Drawn", "Circuit saved as circuit.png")

    def reset(self):
        self.frame.destroy()
        self.gate_sequence = []
        self.init_qubit_selector()

if __name__ == '__main__':
    root = tk.Tk()
    app = QuantumGUI(root)
    root.mainloop()
