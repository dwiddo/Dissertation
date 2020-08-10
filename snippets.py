import numpy as np
import ase_tools

def fit_plane(atoms):
	"""
	given ase.atoms object, find plane of best fit of atoms
	"""
	atoms = ase_tools.unwrap(atoms)
	points = atoms.get_positions()
	points = np.transpose(points)
	points = np.transpose(np.transpose(points) - np.sum(points,1) / len(np.transpose(points))) # subtract out the centroid
	svd = np.transpose(np.linalg.svd(points)) # singular value decomposition
	svd [1] [2] # least singular value
	np.transpose(svd [0]) [2] # the corresponding left singular vector is the normal vector of the best-fitting plane
	normal = np.transpose(svd[0])[2]

def compare_centers(atoms, eps=np.float32(1e-5)):
	"""
	
	"""
	cell = atoms.get_cell()
	cart_to_fract = np.linalg.inv(cell.array)	# change of basis matrix
	centers = ase_tools.get_component_centers(atoms)
	scaled_centers = np.matmul(centers, cart_to_fract)
	pairs = []
	for i, c in enumerate(scaled_centers):
		for c_ in scaled_centers[i+1:]:
			x = np.absolute(c_ - c)
			if np.any(x < eps):
				pairs.append((c, c_))

	return pairs

if __name__ == '__main__':
	import os
	# from ase.io import read
	# import ase
	# from draw import draw
	# from pymatgen.io.ase import AseAtomsAdaptor

	# "job_03351.cif" simplest crystal
    # "job_06871.cif" largest volume
    # "job_06467.cif" most atoms

	"""
		reads from param_data csv file, cuts outliers, and writes
		raw params back into a csv file.
	"""
	# import csv
	#
	# filename = "pow(px,0.35076971).csv"
	# src = os.path.join("Data/function_data_csv", filename)
	# data = []
	# exclude = 4
	# with open(src) as f:
	#     reader = csv.reader(f)
	#     next(reader)
	#     next(reader)
	#     for line in reader:
	#         data.append([float(x) for x in line[1:4]])
	#
	# # trim the data
	# data = np.array(data)
	# # sums = np.sum(data, axis=-1)
	# # cut_data = np.delete(data, np.argsort(sums)[-4:], axis=0)		
	# # data = data[abs(sums-np.mean(sums)) < 4 * np.std(sums)]
	#
	# # print(cut_data.shape, cut_data)
	#
	# path = os.path.join("Data/raw_parameters_csv", filename)
	# with open(path, "w", newline='') as f:
	# 	writer = csv.writer(f)
	# 	writer.writerow(("a", "b", "p"))
	# 	for line in data:
	# 		writer.writerow(line)
	
	import matplotlib.pyplot as plt
	import matplotlib.colors as colors
	import csv

	path = 'Data\params_only_csv\p1+p2pow(x,p3).csv'
	data = []
	with open(path) as file:
		reader = csv.reader(file)
		next(reader)
		for line in reader:
			data.append([float(x) for x in line])
	data = np.array(data)
	clr = data[:,2]
	plt.scatter(data[:,0], data[:,1], s=5, c=clr, cmap='seismic', 
				norm=colors.PowerNorm(gamma=0.5)
				# norm = colors.LogNorm(vmin=clr.min(), vmax=clr.max())
				)
	plt.colorbar()
	plt.show()