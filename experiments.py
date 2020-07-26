from ase.io import read
import os
import numpy as np
import ase_tools
import ase_plotter
import ase

def fit_plane(atoms):
	atoms = ase_tools.unwrap_atoms_from_cell(atoms)
	points = atoms.get_positions()
	points = np.transpose(points)
	points = np.transpose(np.transpose(points) - np.sum(points,1) / len(np.transpose(points))) # subtract out the centroid
	svd = np.transpose(np.linalg.svd(points)) # singular value decomposition
	svd [1] [2] # least singular value
	np.transpose(svd [0]) [2] # the corresponding left singular vector is the normal vector of the best-fitting plane
	normal = np.transpose(svd[0])[2]

def compare_centers(atoms, eps=np.float32(1e-5)):
	positions = atoms.get_positions()
	cell = atoms.get_cell()
	cart_to_fract = np.linalg.inv(cell.array)	# change of basis matrix
	centers = ase_tools.get_component_centers(atoms, unwrap=True)
	scaled_centers = np.matmul(centers, cart_to_fract)
	pairs = []
	for i, c in enumerate(scaled_centers):
		for c_ in scaled_centers[i+1:]:
			x = np.absolute(c_ - c)
			if np.any(x < eps):
				pairs.append((c, c_))
	return pairs

if __name__ == '__main__':
	# "job_03351.cif" simplest crystal
    # "job_06871.cif" largest volume
    # "job_06467.cif" most atoms
	from ase import neighborlist
	from scipy import sparse
	import networkx as nx
	import matplotlib.pyplot as plt
	import ase_plotter

	CIF_DIRECTORY = "T2experimental/"

	atoms = read(os.path.join(CIF_DIRECTORY, "NAVXUG_1478356_T2alpha.cif"))
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ase_plotter.draw(atoms, ax)
	plt.show()
	plt.close()
