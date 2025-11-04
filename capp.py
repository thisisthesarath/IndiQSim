import tkinter as tk
from tkinter import ttk, messagebox
from circuit import QuantumCircuit
from gates import H, X, Y, Z
from utils.circuit_visualizer import draw_circuit
from utils.visualizer import plot_amplitudes
from utils.measurement import measure

GATE_COLORS = {
    "H": "lightblue",
    "X": "lightgreen",
    "Y": "khaki",
    "Z": "lightcoral",
    "CX": "orange"
}

class QuantumGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IndiQSim - Quantum Simulator")

        self.gate_sequence = []
        self.num_qubits = 2  # default

        self.selected_gate = tk.StringVar(value="H")
        self.qubit_options = [i for i in range(5)]
        self.selected_target = tk.IntVar(value=0)
        self.selected_control = tk.IntVar(value=1)

        self.create_widgets()
        self.build_canvas()

    def create_widgets(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Qubits:").grid(row=0, column=0)
        self.qubit_select = ttk.Combobox(control_frame, values=[1, 2, 3, 4, 5], width=5, state="readonly")
        self.qubit_select.set(self.num_qubits)
        self.qubit_select.grid(row=0, column=1)

        tk.Label(control_frame, text="Gate:").grid(row=0, column=2)
        ttk.Combobox(control_frame, values=["H", "X", "Y", "Z", "CX"], textvariable=self.selected_gate, width=5).grid(row=0, column=3)

        tk.Label(control_frame, text="Target:").grid(row=0, column=4)
        self.target_entry = ttk.Combobox(control_frame, values=self.qubit_options, textvariable=self.selected_target, width=5)
        self.target_entry.grid(row=0, column=5)

        tk.Label(control_frame, text="Control:").grid(row=0, column=6)
        self.control_entry = ttk.Combobox(control_frame, values=self.qubit_options, textvariable=self.selected_control, width=5)
        self.control_entry.grid(row=0, column=7)

        tk.Button(control_frame, text="Add Gate", command=self.add_gate).grid(row=0, column=8, padx=10)
        tk.Button(control_frame, text="Reset", command=self.reset).grid(row=0, column=9, padx=5)
        tk.Button(control_frame, text="Simulate", command=self.simulate).grid(row=0, column=10, padx=5)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack()

    def build_canvas(self):
        self.num_qubits = int(self.qubit_select.get())
        self.canvas_width = 1000
        self.canvas_height = 80 * self.num_qubits

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        # Draw horizontal qubit lines
        for q in range(self.num_qubits):
            y = 60 + q * 60
            self.canvas.create_line(50, y, self.canvas_width - 50, y)
            self.canvas.create_text(30, y, text=f"q{q}", font=("Arial", 12, "bold"))

        # Reset circuit and gate sequence
        self.qc = QuantumCircuit(self.num_qubits)
        self.gate_sequence = []

        # Update dropdown options
        self.qubit_options = [i for i in range(self.num_qubits)]
        self.target_entry.config(values=self.qubit_options)
        self.control_entry.config(values=self.qubit_options)

    def add_gate(self):
        gate = self.selected_gate.get()
        tgt = self.selected_target.get()

        if gate in ["H", "X", "Y", "Z"]:
            if tgt >= self.num_qubits:
                messagebox.showerror("Invalid", f"Qubit {tgt} doesn't exist.")
                return
            getattr(self.qc, 'apply_gate')(globals()[gate], tgt)
            self.gate_sequence.append({"gate": gate, "target": tgt})
            self.draw_gate(gate, tgt)
        elif gate == "CX":
            ctrl = self.selected_control.get()
            if ctrl >= self.num_qubits or tgt >= self.num_qubits or ctrl == tgt:
                messagebox.showerror("Invalid", "Control and Target must be different and valid.")
                return
            self.qc.apply_cx(ctrl, tgt)
            self.gate_sequence.append({"gate": "CX", "control": ctrl, "target": tgt})
            self.draw_cx(ctrl, tgt)

    def draw_gate(self, gate, q):
        step = len(self.gate_sequence)
        x = 100 + step * 60
        y = 60 + q * 60
        self.canvas.create_rectangle(x-15, y-15, x+15, y+15, fill=GATE_COLORS[gate])
        self.canvas.create_text(x, y, text=gate)

    def draw_cx(self, ctrl, tgt):
        step = len(self.gate_sequence)
        x = 100 + step * 60
        y_ctrl = 60 + ctrl * 60
        y_tgt = 60 + tgt * 60
        self.canvas.create_line(x, y_ctrl, x, y_tgt)
        self.canvas.create_oval(x-5, y_ctrl-5, x+5, y_ctrl+5, fill="black")
        self.canvas.create_oval(x-12, y_tgt-12, x+12, y_tgt+12, fill=GATE_COLORS["CX"])
        self.canvas.create_text(x, y_tgt, text="X")

    def reset(self):
        self.build_canvas()

    def simulate(self):
        print("Final State Vector:\n", self.qc.state)
        counts = measure(self.qc.state, 1024)
        print("Measurement Counts:\n", counts)
        plot_amplitudes(self.qc.state)
        draw_circuit(self.num_qubits, self.gate_sequence)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumGUI(root)
    root.mainloop()
