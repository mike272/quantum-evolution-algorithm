import numpy as np

from typing import List, Any


class FloatQubit:
    alpha = 0
    beta = 0
class FloatQubyte:
    qubites: list[FloatQubit] = []

class Layer:
    def __init__(self, weights: np.ndarray | List[FloatQubit]):
        self.size = len(weights)
        self.weights = weights
