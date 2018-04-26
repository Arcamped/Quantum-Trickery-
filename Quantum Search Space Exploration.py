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
import csv
from matplotlib import pyplot as plt
qvm = QVMConnection()

number = 2 # Sets number of qubits to use. Hardware limited to <= 19 (18?)
trials = 1000  # Number of search space simulations to run.
depth = 30 # How deep each search is allowed to go (the number of draws).
def n_qubits (number) :
    ''' takes as argument the number of qubits to apply Hadamard Gates to
    and measure. Outputs a concatenated string of measurements.'''
    q = Program()
    [q.inst(H(entry)) for entry in range(number)]
    [q.measure(entry, entry) for entry in range(number)]
    wavefunction3 = qvm.wavefunction(q, classical_addresses=range(number))
    classical_mem3 = wavefunction3.classical_memory
    #print (classical_mem3)
    return("".join([str(x) for x in classical_mem3]))

# Runs the simulations at the depth specified and store results in a csv and
# a list of lists (master1).
master1 = [[] for j in range(trials)]
for j in range(trials) :
    #global container
    container = []
    for i in range(depth) :
        ''' Randomly generates results from search space until space is exhausted
            or the maximum number of iterations is reached'''
        if len(set(container)) < number ** 2 :
            results = (n_qubits(number))
            container.append(results)
        else :
            results = 0
            container.append(results)
        master1[(j)] = container
with open("output1.csv",'w', newline='') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    for value in master1:
        wr.writerow([value])

# Turn master1 into DataFrame for manipulation/analysis.
df_results = pd.DataFrame(master1)
df_results = df_results.transpose()
df_results.index += 1
df_results.shape

# Identifies how long it took each trial to reach exhaustion.
# There has to be a better way to find exhaustion?
counter = []
for i in df_results:
    place = (df_results[i] == 0).sum()
    print((df_results[i] == 0).sum())
    counter.append(place)
len(counter)
UTTE = depth - sum(counter)/trials
print(UTTE)

# Visual inspection of data.
unique_counter = list(set(counter))
print(unique_counter)

# Subtracts the number of zeros from 30 to get the number of steps it took to
# reach search space exhaustion
adjusted_counter[:] = [depth - value for value in counter]

# Checking to make sure the list didn't lose any values
adjusted_counter_unique = list(set(adjusted_counter))
print(adjusted_counter_unique)

#Need to set minimum bound as far left on graph. Where minimum bound is
# number ** 2 representing a perfectly efficient search.
plt.hist(adjusted_counter, bins = depth - number ** 2)
plt.xlabel( x='Number of Draws Until Exhaustion')

# This saves the results of the simulation.
# (# qubits_#trials_#depth of each trial)
df_results.to_pickle('2q_1000t_30d')

# Histogram display problems... should be fixable if bins start at lower bound
adjusted_counter.count(21)

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
