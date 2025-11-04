import matplotlib.pyplot as plt

def draw_circuit(num_qubits, gate_sequence, save_path="circuit.png"):
    fig, ax = plt.subplots(figsize=(max(6, len(gate_sequence)), 1 + 0.5 * num_qubits))
    ax.axis('off')

    spacing = 1
    x = 1

    # Draw qubit lines
    for q in range(num_qubits):
        ax.hlines(y=q, xmin=0.5, xmax=len(gate_sequence) + 1, color='black')
        ax.text(0, q, f'q{q}', fontsize=12, ha='right', va='center')

    for step, gate in enumerate(gate_sequence):
        gtype = gate["gate"]
        if gtype == "H":
            ax.text(x, gate["target"], "H", bbox=dict(boxstyle='round', facecolor='lightblue'), ha='center', va='center')
        elif gtype == "X":
            ax.text(x, gate["target"], "X", bbox=dict(boxstyle='round', facecolor='lightgreen'), ha='center', va='center')
        elif gtype == "Z":
            ax.text(x, gate["target"], "Z", bbox=dict(boxstyle='round', facecolor='lightcoral'), ha='center', va='center')
        elif gtype == "Y":
            ax.text(x, gate["target"], "Y", bbox=dict(boxstyle='round', facecolor='khaki'), ha='center', va='center')
        elif gtype == "CX":
            ctrl = gate["control"]
            tgt = gate["target"]
            ax.plot([x, x], [ctrl, tgt], color='black', linestyle='-', linewidth=2)
            ax.plot(x, ctrl, 'o', color='black')
            ax.text(x, tgt, 'X', bbox=dict(boxstyle='circle', facecolor='orange'), ha='center', va='center')

        x += 1

    ax.set_ylim(-1, num_qubits)
    ax.set_xlim(0, x)
    plt.title("Quantum Circuit")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Circuit saved as {save_path}")
