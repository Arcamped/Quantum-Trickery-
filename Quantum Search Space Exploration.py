# The goal is to use parametric gates (or QFTs?) to reduce the mean number of draws required to find all possible
# outcomes in a search space. The intent is to make changes to the wavefunction and the
# probability amplitudes for each qubit to bias the system away from previously measured values.

# To do:
### QFT vs CR gates. Resource advantage for either?
### Issue of noisy measurements?
### Monte Carlos for unmodified time to mean (UTTM?)


from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.gates import H
import numpy as np
qvm = QVMConnection()

number = 3 # Sets number of qubits to apply gates to and measure. Hardware limited to <= 19 (18?)

def n_die (number) :
    ''' takes as argument the number of qubits to apply Hadamard Gates to
    and measure. Outputs a concatenated string of results.'''
    q = Program()
    [q.inst(H(entry)) for entry in range(number)]
    [q.measure(entry, entry) for entry in range(number)]
    wavefunction3 = qvm.wavefunction(q, classical_addresses=range(number))
    classical_mem3 = wavefunction3.classical_memory
    #print (classical_mem3)
    return("".join([str(x) for x in classical_mem3]))


print(n_die(number))


quantum_dict = {}
# Dictionary generation and storage method. Cute, but not of a ton of use(?).
for i in range(10) :
    ''' Populates quantum_dict with n_die(number) draws until all possible states
    are drawn or the specified number of iterations in range() is reached.'''
    result = n_die(number)
    if result not in quantum_dict.keys() and len(quantum_dict) < number ** 2 : #
        quantum_dict[result] = i + 1
        print(result)
    elif len(quantum_dict) < number ** 2 :
        print(result + " is a repeat") #For debugging purposes. Also a reminder to think about noise.
    elif len(quantum_dict) == number ** 2 :
        break

print(quantum_dict)

# This list stores results in order n_die(number) generates them.
holder = []
print(n_die(number))
for i in range(10) :
    results = (n_die(number))
    print(results)
    holder.append(results)

print(holder)


# Much of the above workflow is the same, but using the Hadamard Gate (H()) is no longer appropriate.
# Instead, parametric gates will be used and updated between measurements.
# Using the cartesian rotation gate of the form:

from pyquil.parameters import Parameter, quil_sin, quil_cos
from pyquil.quilbase import DefGate
from pyquil.gates import *
from math import pi
import numpy as np

theta = Paramter('theta')
crx = np.array([[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, quil_cos(theta/2), -1j * quil_sin(theta/2)],
                 [0, 0, -1j * quil_sin(theta/2), quil_cos(theta/2)]])

dg = DefGate('CRX', crx, [theta])
CRX = dg.get_constructor()


# Would it make more sense to use QFT? Depends on how entanglement is used?

def qft3(q0, q1, q2):
    p = Program()
    p.inst( H(q2),
        CPHASE(pi/2.0, q1, q2),
        H(q1),
        CPHASE(pi/4.0, q0, q2),
        CPHASE(pi/2, q0, q1),
        H(q0),
        SWAP(q0, q2) )
    return p

print(qft3(0, 1, 2))
