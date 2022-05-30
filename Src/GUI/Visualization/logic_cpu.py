import numpy as np
from random import random
from typing import List, Tuple
from Src.GUI.Visualization.layer import *

from Src.const import COW_JUMP_POWER, PIPE_DIST, SCREEN_SIZE

def preprocessInput(input: List[float]) -> np.ndarray:
    arr = np.zeros((2), dtype=np.float16)

    arr[0] = input[0]/SCREEN_SIZE[1]
    arr[1] = input[1]/COW_JUMP_POWER

    return arr

def createNFloats(input: str, n: int, precision: int, offset: int = 0) -> Tuple[np.ndarray,int]:
    arr = np.zeros((n), dtype=np.float16)
    for i in range(0, n):
        s = input[offset+i*precision:offset+(i+1)*precision]
        sign = 1 if int(s[0]) == 0 else -1
        val = int(s[1:], base=2) / (2**precision-1)
        f = sign/val if val!=0 else 0
        arr[i] = f
    
    return (arr,offset+n*precision)


def multiply(input:np.ndarray, weights: np.ndarray) -> float:
    return np.dot(input, weights)

def map(input: float) -> bool:
    return input>=0.5 

def mutateBits(s:str, m:float):
    o = ""

    for i in range(0, len(s)):
        if(random()<m):
            if(s[i] == "0"):
                o+="1"
            else:
                o += "0"
        else:
            o+=s[i]

    return o  
