import ase.io
import os
from scipy.spatial import Voronoi
import numpy as np

# set path to the directory containing cif file
# leave as '' if file is in same directory as this file
path = 'cifs/Large_T2_set'
# path = "cifs/T2_experimental/"
filename = 'job_03351.cif'
# filename = "DEBXIT02_1478361_T2gamma_450K.cif"
atoms = ase.io.read(os.path.join(path, filename))

# atoms = ase.io.read("job_03351.cif")
points = atoms.get_scaled_positions()
vor = Voronoi(points)

import matplotlib.pyplot as plt
from ase_plotter import draw_line

fig = plt.figure()
ax = fig.gca(projection='3d')

# ax.scatter(vor.vertices[:,0], vor.vertices[:,1], vor.vertices[:,2])
for indices in vor.ridge_vertices:
    if all(i >= 0 for i in indices):
        pairs = [(indices[i], indices[(i+1) % len(indices)]) for i in range(len(indices))]
        for pair in pairs:
            if np.linalg.norm(vor.vertices[pair[0]]) < 10 and np.linalg.norm(vor.vertices[pair[1]]) < 10:
                draw_line(vor.vertices[pair[0]], vor.vertices[pair[1]], ax)
ax.set_xlim(-1, 2)
ax.set_ylim(-1, 2)
ax.set_zlim(-1, 2)
plt.show()
