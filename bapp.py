import tkinter as tk
from tkinter import messagebox, filedialog
from circuit import QuantumCircuit
from gates import H, X, Y, Z
from utils.measurement import measure
from utils.visualizer import plot_amplitudes
from utils.circuit_visualizer import draw_circuit
import os

class QuantumGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IndiQSim - Quantum Circuit Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")

        self.num_qubits = tk.IntVar(value=2)
        self.qc = None
        self.gate_sequence = []

        self.create_widgets()

    def create_widgets(self):
        control_frame = tk.Frame(self.root, bg="#1e1e1e")
        control_frame.pack(pady=20)

        tk.Label(control_frame, text="Qubits:", fg="white", bg="#1e1e1e", font=("Arial", 12)).pack(side=tk.LEFT)
        self.qubit_entry = tk.Entry(control_frame, textvariable=self.num_qubits, width=5, font=("Arial", 12))
        self.qubit_entry.pack(side=tk.LEFT, padx=10)

        tk.Button(control_frame, text="Create Circuit", command=self.initialize_circuit, bg="#007acc", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Reset", command=self.reset, bg="#e81123", fg="white").pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.root, bg="#2d2d2d", width=800, height=400)
        self.canvas.pack(pady=10)

        gate_frame = tk.Frame(self.root, bg="#1e1e1e")
        gate_frame.pack()

        self.gates = ["H", "X", "Y", "Z", "CX"]
        for gate in self.gates:
            btn = tk.Button(gate_frame, text=gate, width=5, command=lambda g=gate: self.apply_gate_ui(g), bg="#3a3a3a", fg="white")
            btn.pack(side=tk.LEFT, padx=5)

        action_frame = tk.Frame(self.root, bg="#1e1e1e")
        action_frame.pack(pady=10)
        
        tk.Button(action_frame, text="Measure", command=self.measure, bg="#007acc", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(action_frame, text="Export Qiskit Code", command=self.export_qiskit, bg="#00cc6a", fg="white").pack(side=tk.LEFT, padx=10)

    def initialize_circuit(self):
        try:
            n = self.num_qubits.get()
            if n < 1 or n > 5:
                raise ValueError("1 <= qubits <= 5")
            self.qc = QuantumCircuit(n)
            self.gate_sequence = []
            self.draw_circuit()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def apply_gate_ui(self, gate):
        if not self.qc:
            messagebox.showwarning("Warning", "Create a circuit first")
            return

        if gate == "CX":
            ctrl = self.ask_qubit("Control Qubit Index")
            tgt = self.ask_qubit("Target Qubit Index")
            if ctrl is None or tgt is None:
                return
            self.qc.apply_cx(ctrl, tgt)
            self.gate_sequence.append({"gate": "CX", "control": ctrl, "target": tgt})
        else:
            q = self.ask_qubit(f"Apply {gate} to qubit")
            if q is None:
                return
            gate_obj = eval(gate)
            self.qc.apply_gate(gate_obj, q)
            self.gate_sequence.append({"gate": gate, "target": q})

        self.draw_circuit()

    def ask_qubit(self, prompt):
        try:
            return int(tk.simpledialog.askstring("Input", prompt))
        except:
            return None

    def draw_circuit(self):
        draw_circuit(self.qc.num_qubits, self.gate_sequence, save_path="gui/circuit.png")
        self.show_image("gui/circuit.png")

    def show_image(self, path):
        from PIL import Image, ImageTk
        img = Image.open(path)
        img = img.resize((800, 400), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def measure(self):
        if not self.qc:
            messagebox.showwarning("Warning", "Create a circuit first")
            return
        counts = measure(self.qc.state, 1024)
        messagebox.showinfo("Measurement", str(counts))
        plot_amplitudes(self.qc.state)

    def export_qiskit(self):
        if not self.gate_sequence:
            messagebox.showwarning("Warning", "Build a circuit first")
            return

        lines = ["from qiskit import QuantumCircuit\n",
                 f"qc = QuantumCircuit({self.qc.num_qubits})\n"]

        for gate in self.gate_sequence:
            if gate["gate"] == "CX":
                lines.append(f"qc.cx({gate['control']}, {gate['target']})\n")
            else:
                lines.append(f"qc.{gate['gate'].lower()}({gate['target']})\n")

        lines.append("qc.measure_all()\n")

        filename = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
        if filename:
            with open(filename, 'w') as f:
                f.writelines(lines)
            messagebox.showinfo("Exported", f"Qiskit code saved to {filename}")

    def reset(self):
        self.num_qubits.set(2)
        self.qc = None
        self.gate_sequence = []
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumGUI(root)
    root.mainloop()
