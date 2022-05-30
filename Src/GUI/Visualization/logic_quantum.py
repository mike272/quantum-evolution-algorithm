from typing import List, Tuple
from Src.GUI.Visualization.layer import *
from Src.settings import Settings

def preprocessInputQ(input: List[float], settings:Settings) -> List[FloatQubit]:
    return []

def createNFloatsQ(input: str, n: int, precision: int, offset: int = 0) -> Tuple[List[FloatQubit],int]:
    return ([],offset+n*precision)

def multiplyQ(input: List[FloatQubit], weights: List[FloatQubit]) -> FloatQubit:
    return FloatQubit()

def mutateBitsQ(s:str, m:float):
    return s

def mapQ(input: FloatQubit) -> bool:
    return True