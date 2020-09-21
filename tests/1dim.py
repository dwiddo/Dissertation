import numpy as np
import random
import math

def get_AMDs(lattice_vector, motif_size, lattice_len):

    motif = [random.uniform(0.0,1.0) * lattice_vector for _ in range(motif_size)]
    lattice = [lattice_vector * n for n in range(-lattice_len, lattice_len)]
    S = [l + m for l in lattice for m in motif]
    shifted_S = []
    for m in motif:
        shift = []
        for s in S:
            t = m - s if s - m < 0 else s - m
            shift.append(t)
        shifted_S.append(sorted(shift))
    shifted_S = np.array(shifted_S)
    AMDs = shifted_S.mean(axis=0)
    return AMDs


import matplotlib.pyplot as plt


# plt.plot(y_lower)
# plt.plot(y_upper)

fig, (ax1, ax2) = plt.subplots(1, 2)
plt.rcParams.update({'font.size': 20})

max_k = 100

v = 1
M = 3
L = 500
amds1 = get_AMDs(v, M, L)
ax1.plot(amds1[0:max_k], 'k', label='AMD$_k$', linewidth=3)
ax1.plot([(k) / (2 * M) * v for k in range(max_k)], linewidth=3, label=r'$\frac{kv}{2|M|}$')
ax1.set(xlabel="$k$")
ax1.legend()

v = 1
M = 10
L = 500
amds2 = get_AMDs(v, M, L)
ax2.plot(amds2[0:max_k], 'k', label='AMD$_k$', linewidth=3)
ax2.plot([(k) / (2 * M) * v for k in range(max_k)], linewidth=3, label=r'$\frac{kv}{2|M|}$')
ax2.set(xlabel="$k$")
ax2.legend()
plt.show()