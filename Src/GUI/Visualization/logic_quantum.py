from typing import List, Tuple

class FloatQubit:
    pass


def preprocessInputQ(input: List[float]) -> List[FloatQubit]:
    return []

def createNFloatsQ(input: str, n: int, precision: int, offset: int = 0) -> Tuple[List[FloatQubit],int]:
    return ([],offset+n*precision)

def multiplyQ(input: List[FloatQubit], weights: List[FloatQubit]) -> FloatQubit:
    return FloatQubit()

def mapQ(input: FloatQubit) -> bool:
    return True