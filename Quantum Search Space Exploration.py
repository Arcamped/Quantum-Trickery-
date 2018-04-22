# The goal is to use parametric gates (or QFTs?) to reduce the mean number of draws required to find all possible
# outcomes in a search space. The intent is to make changes to the wavefunction and the
# probability amplitudes for each qubit to bias the system away from previously measured values.

### To do:
# QFT vs CR gates. Resource advantage for either?
# Issue of noisy measurements?
# Monte Carlos for unmodified time to exhaustion (UTTE?)
# Entanglement usage?


from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.gates import H
import numpy as np
import pandas as pd
qvm = QVMConnection()

number = 2 # Sets number of qubits to use. Hardware limited to <= 19 (18?)

def n_die (number) :
    ''' takes as argument the number of qubits to apply Hadamard Gates to
    and measure. Outputs a concatenated string of measurements.'''
    q = Program()
    [q.inst(H(entry)) for entry in range(number)]
    [q.measure(entry, entry) for entry in range(number)]
    wavefunction3 = qvm.wavefunction(q, classical_addresses=range(number))
    classical_mem3 = wavefunction3.classical_memory
    #print (classical_mem3)
    return("".join([str(x) for x in classical_mem3]))

print(n_die(number))


# There appears to be an issue when one simulation runs longer than the others.
# Error: "ValueError: Length of values does not match length of index"
trials = 2
df_trials = pd.DataFrame()
container = []

for j in range(trials) :
    global container
    container = []
    for i in range(15) :
        ''' Randomly generates results from search space until space is exhausted
            or the maximum number of iterations is reached'''
        if len(set(container)) < number ** 2 :
            results = (n_die(number))
            container.append(results)
        else :
            break
    df_trials[j] = container
print(container)
df_trials.shape
print(df_trials)
# Much of the above workflow is the same, but using the Hadamard Gate (H()) is no
# longer appropriate beyond first measurement.
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






### Redundnat code kept around for example purposes and proofreading work:

# This list stores results in the order n_die(number) generates them.
holder = []

for i in range(15) :
    ''' Randomly generates results from search space until space is exhausted
        or the maximum number of iterations is reached'''
    if len(set(holder)) < number ** 2 :
        results = (n_die(number))
        holder.append(results)
    else :
        break

print(holder)


quantum_dict = {}
# Dictionary generation and storage method.
# Currently, this code is of no use.
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
