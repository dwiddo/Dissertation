import numpy as np
import ase_tools
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import csv

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



def read_csv_(path, split_names=None, omit_names=None):
	"""
	very specific function for reading csv in the format found in
	Data\parameter_data_csv directory.
	Optionally split can be a list of names (first column) to seperate out
	and return in data_, so they can be highlighted on a graph.
	"""
	if split_names is None:
		split_names = []
	if omit_names is None:
		omit_names = []

	with open(path) as file:
		reader = csv.reader(file)
		next(reader)
		data = []
		data_ = []

		for line in reader:
			if line[0] not in omit_names:
				if line[0] in split_names:
					data_.append([float(x) for x in line[1:4]])
				else:
					data.append([float(x) for x in line[1:4]])
	
	if split_names is None:
		return np.array(data), None
	else:
		return np.array(data), np.array(data_)


		# if split_names is None:
		# 	for i, line in enumerate(reader):
		# 		if line[0] not in ignore_names:
		# 			data.append([float(x) for x in line[1:4]])
		# 	return np.array(data), None
		# else:
		# 	data_ = []
		# 	for line in reader:
		# 		if line[0] not in ignore_names:
		# 			if line[0] in split_names:
		# 				data_.append([float(x) for x in line[1:4]])
		# 			else:
		# 				data.append([float(x) for x in line[1:4]])
		# 	return np.array(data), np.array(data_)

def flatten_colour_scatter_label(path, ax, highlight_names=None, omit_names=None):
	"""
	very specific function, as the above is.
	Takes path to csv in format found in directory Data\parameter_data_csv
	(skip first two lines, columns are name,p1,p2,p3,etc)
	plots a scatter with p1 on x-axis, p2 on y-axis. colour gradient is then
	applied according to p3.
	"""

	data, label_data = read_csv_(path, split_names=highlight_names, omit_names=omit_names)
	X = data[:,0]
	Y = data[:,1]
	clr = data[:,2]

	im = ax.scatter(X, Y, s=3, c=clr, cmap='inferno',
				norm=colors.PowerNorm(gamma=0.5)
				# norm=colors.LogNorm(vmin=clr.min(), vmax=clr.max())
				)
	if label_data is not None:
		ax.scatter(label_data[:,0], label_data[:,1], s=4, c='k')
		# arrived at offsets manually
		offsets = [(-50,-10), (3,0), (-55,0), (-20,-12), (3,0), (3,0), (3,0)]

		X_ = label_data[:,0]
		Y_ = label_data[:,1]
		for i, name in enumerate(highlight_names):
			ax.annotate(name, (X_[i], Y_[i]), xytext=offsets[i], textcoords='offset points')
	
	return im


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
	# # metric = ...
	# # cut_data = np.delete(data, np.argsort(metric)[-4:], axis=0)		
	# # data = data[abs(metric-np.mean(metric)) < 4 * np.std(metric)]


	path = 'Data\parameter_data_csv\p1+p2pow(x,p3).csv'

	highlight_names = ['job_00001', 'job_00014', 'job_00015', 'job_00054', 'job_00120', 'job_00186', 'job_05926']
	# omit_names = ['job_04117']
	omit_names = None

	fig, ax = plt.subplots()

	im = flatten_colour_scatter_label(path, ax, highlight_names=highlight_names, omit_names=omit_names)

	plt.xlabel('a')
	plt.ylabel('b')
	plt.title("a+b*x^p")
	cbar = fig.colorbar(im, ax=ax)
	cbar.set_label("p")

	plt.show()
