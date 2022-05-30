import numpy as np

from typing import List

class FloatQubit:
    pass

class Layer:
    def __init__(self, weights:np.ndarray|List[FloatQubit]):
        self.size = len(weights)
        self.weights = weights