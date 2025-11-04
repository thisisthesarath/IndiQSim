import numpy as np
import matplotlib.pyplot as plt

def plot_amplitudes(state_vector):
    probs = np.abs(state_vector.flatten())**2
    n = int(np.log2(len(probs)))
    labels = [f"|{i:0{n}b}⟩" for i in range(len(probs))]

    plt.bar(labels, probs)
    plt.title("Quantum State Probabilities")
    plt.ylabel("Probability")
    plt.show()
