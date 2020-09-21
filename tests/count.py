import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import math

# given a lattice, plot k vs kth nearest neighbour to (0,0,0)

def distance(p):
    return sum(x**2 for x in p)

def multirange(dims, m):
    c = 0
    for i in range(m**dims):
        x = i
        r = []
        for n in range(dims):
            x, rem = divmod(x, m)
            r.append(rem)
        yield tuple(r)[::-1]

def generate_N3(limit=None):
    n = 3
    ymax = defaultdict(int) # unknown keys are mapped to 0
    d = 0
    while limit is None or d <= limit:
        yieldable = []
        while 1:
            batch = []
            for x in multirange((n-1), d+1):
                y = ymax[x]
                pt = x + (y,)
                if distance(pt) <= d**2:
                    batch.append(pt)
                    ymax[x] += 1
            if not batch:
                break
            yieldable += batch
        yieldable.sort(key=distance)
        for p in yieldable:
            yield p
        d += 1

def generate_Z3(limit=None):
    for p in generate_N3(limit=limit):
        yield p
        if p[0]: yield -p[0], p[1], p[2]
        if p[1]: yield p[0], -p[1], p[2]
        if p[2]: yield p[0], p[1], -p[2] 
        if p[0] and p[1]: yield -p[0], -p[1], p[2]
        if p[0] and p[2]: yield -p[0], p[1], -p[2]
        if p[1] and p[2]: yield p[0], -p[1], -p[2] 
        if p[0] and p[1] and p[2]: yield -p[0], -p[1], -p[2]

max_k = 10000
t = generate_Z3()
points = [np.sqrt(distance(next(t))) for _ in range(max_k)]

def estimate(k):
    return ((3 * k) / (4 * math.pi)) ** (1/3)

plt.plot(points)
plt.plot([2 * estimate(k) for k in range(max_k)])
plt.show()

# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# X, Y, Z = points[:,0], points[:,1], points[:,2]
# ax.scatter(X, Y, Z)

# ax.set_box_aspect([1,1,1])
# plt.show()

