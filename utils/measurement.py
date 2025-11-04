# utils/measurement.py
import numpy as np
from collections import Counter

def measure(state_vector, shots=1000):
    num_qubits = int(np.log2(len(state_vector)))
    probabilities = np.abs(state_vector.flatten())**2
    outcomes = [format(i, f'0{num_qubits}b') for i in range(len(probabilities))]

    results = np.random.choice(outcomes, size=shots, p=probabilities)
    counts = dict(Counter(results))
    return counts
