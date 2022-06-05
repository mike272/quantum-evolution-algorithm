from typing import List, Tuple

from qiskit.extensions.quantum_initializer.initializer import initialize

from Src.GUI.Visualization.layer import *
from Src.settings import Settings
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, BasicAer
from Src.const import COW_JUMP_POWER, PIPE_DIST, SCREEN_SIZE
import random

from qiskit import transpile

# Use AerSimulator
from qiskit.providers.aer import AerSimulator

def findClosestQFloat(input: float, precision: int) -> float:
    r = 2**(precision-1)
    f = round(input * r)/r
    return f


def preprocessInputQ(input: List[float], settings: Settings) -> List[FloatQubit]:
    # qc = QuantumCircuit()
    arr = np.zeros((2), dtype=np.float16)

    arr[0] = findClosestQFloat(input[0] / SCREEN_SIZE[1], settings.float_precision)
    arr[1] = findClosestQFloat(input[1] / COW_JUMP_POWER, settings.float_precision)

    # print(arr)
    return arr

    return []


def dropQtoB(qubit) -> int:
    sumSq = qubit[0] ** 2 + qubit[1] ** 2
    if (qubit[0] / sumSq > 0.5):
        return 1
    return 0

def stringToQbytes(input:str, n: int, precision: int, offset: int = 0):
    for i in range(0, n):
        s = input[offset + i * precision:offset + (i + 1) * precision]
#         fuck me if I know what i'm doing here
#         I guess I should be taking probabilites instead of string of bits

def createNFloatsQ(input, n: int, precision: int, offset: int = 0) -> Tuple[np.ndarray, int]:
    # convert str to qubytes
    # array = np.zeros((n, 2), dtype=np.float16)
    # for i in range(0, n):
    #     # object with 5 qubits
    #     s: FloatQubyte = input[i]
    #     tmp = np.zeros(5)
    #     for j in range(0, 5):
    #         # measuring bits
    #         tmp[j] = dropQtoB(s.qubites[j])
    #
    #     sign = 1 if int(tmp[0]) == 0 else -1
    #     val = int(tmp[1:], base=2) / (2 ** precision - 1)
    #     f = sign / val if val != 0 else 0
    #     array[i] = f
    #
    # return (array, offset + n * precision)
    arr = np.zeros((n), dtype=np.float16)
    for i in range(0, n):
        s = input[offset+i*precision:offset+(i+1)*precision]
        sign = 1 if int(s[0]) == 0 else -1
        val = int(s[1:], base=2) / (2**precision-1)
        f = sign/val if val!=0 else 0
        arr[i] = f

    return (arr,offset+n*precision)



def multiplyQ(input: List[FloatQubit], weights: List[FloatQubit]) -> FloatQubit:
    return np.dot(input, weights)


def mutateBitsQ(s:str, m:float):
    return s


def mapQ(input: float) -> bool:
    return input>=0.5

#########################################################
# QUANTUM ROTATION GATE                                 #
#########################################################
def rotation(s:str, settings:Settings):
    backend = AerSimulator()

    creg = ClassicalRegister(len(s))
    qreg = QuantumRegister(len(s))
    circ = QuantumCircuit(len(s))
    reversed_str = s[::-1]
    # qc.initialize(reversed_str, qreg)
    for i in range(0, len(s)):
        circ.h(i)
        circ.rx(50, i)
        circ.ry(50, i)
        circ.rz(50, i)

        meas = QuantumCircuit(10, 10)
        meas.barrier(range(10))
        # map the quantum measurement to the classical bits
        meas.measure(range(10), range(10))

        # The Qiskit circuit object supports composition.
        # Here the meas has to be first and front=True (putting it before)
        # as compose must put a smaller circuit into a larger one.
        qc = meas.compose(circ, range(10), front=True)
        qc_compiled = transpile(qc, backend)
    job_sim = backend.run(qc_compiled, shots=19)
    result_sim = job_sim.result()
    counts = result_sim.get_counts(qc_compiled)
    print(counts)
    return counts

    # Grab the results from the job.
    # result_sim = job_sim.result()
    # qc.measure(qreg, creg)
    # print(creg)
    # res = ""
    # for i in range(len(s)-1, 0, -1):
    #     res = res+str(creg[i])
    # print(res)
    # return res

