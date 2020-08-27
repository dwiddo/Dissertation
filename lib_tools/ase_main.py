from ase.io import read
import os
from scipy.spatial import Voronoi
import numpy as np


# set path to the directory containing cif file
# path = 'cifs/Large_T2_set'
# filename = 'job_00001.cif'
path = "Data/cifs/T2_experimental/"
filename = "DEBXIT02_1478361_T2gamma_450K.cif"
atoms = read(os.path.join(path, filename))
import draw
draw.draw(atoms, unwrap=False)
