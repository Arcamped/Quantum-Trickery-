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
import matplotlib.pyplot as plt
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
df_results.index += 1

# Add column holding mean time to exhaustion by subtracting number of 0s from
# depth of search. recall 0s are automatically written when unique results = number ** 2.
df_results['exhaustion'] = df_results.apply(lambda row: depth - sum(row[:]==0) ,axis=1)


# Load chosen data:
df_results = pd.read_pickle('2q_1000t_30d_1')
df_results['exhaustion'].plot(kind='hist', bins = depth - number ** 2)
print(df_graph)

# plt.show() is still empty.... And still can't axis labels because plt.show doesn't work...
df_graph = df_results[['exhaustion']]
df_graph.plot(kind='hist', bins = depth - number ** 2, xlim=([4,30]))


import pickle
# Save data frame for later
# (# qubits_# of trials_depth of each trial_trial iteration number)
df_results.to_pickle('2q_1000t_30d_1.pkl')


# Much of the above workflow is the same, but using the Hadamard Gate (H()) is no
# longer appropriate beyond first measurement.


## The objective is to adjust the wavefunctions appropriately so that the
# modified time to exhaustion (MTTE) is < the UTTE. Obviously, given complete control
# over probability amplitudes and perfect knowledge of past draws would
# allow MTTE = number ** 2. Thus, allowed deviation from the 50-50 superposition
# imposed by the Hadamard gate will be restricted to some set value dependent on
# system size(?).

print(1/ np.sqrt(2))
print(wavefunction.amplitudes)

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
