import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import csv

import sys
sys.path.append('.')
from lib_tools import ase_tools

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



def read_csv_(path, split_names=None, omit_names=None, names_col=0, col_start=1, col_end=4):
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
			if line[names_col] not in omit_names:
				data_point = [float(x) for x in line[col_start:col_end]]
				if line[names_col] in split_names:
					data_.append(data_point)
				else:
					data.append(data_point)
	
	if split_names is None:
		return np.array(data), None
	else:
		return np.array(data), np.array(data_)

def flatten_colour_label_scatter(data, ax, data_=None, labels=None):
	"""
	:param: data 
		np array of shape (n,3)
	:param: ax
		matplotlib axes object to draw to
	:param: data_
		np array of shape (n,3)
	:param: labels
		container of strings the same length as data_ 
		(len(labels) == data.shape[0])
		
	:return:
		matplotlib PathCollection object returned from scatter. Useful to add colourbar.
	"""

	X = data[:,0]
	Y = data[:,1]
	clr = data[:,2]

	im = ax.scatter(X, Y, s=1, c=clr, label='_nolegend_', cmap='viridis',
				    # norm=colors.PowerNorm(gamma=2)
				    # norm=colors.LogNorm(vmin=clr.min(), vmax=clr.max())
				   )

	if data_ is not None:
		markers = ['o', '^', 's', 'P', '*', 'X', 'd']
		for i, point in enumerate(data_):
			ax.scatter(point[0], point[1], s=30, c='k', 
					   marker=markers[i % len(markers)])
		ax.legend(labels)

	return im


if __name__ == '__main__':
	import os
	# from ase.io import read
	# import ase
	# from pymatgen.io.ase import AseAtomsAdaptor

	# "job_03351.cif" simplest crystal
    # "job_06871.cif" largest volume
    # "job_06467.cif" most atoms

	"data cutting code"
	# metric = ...
	# cut_data = np.delete(data, np.argsort(metric)[-4:], axis=0)
	# data = data[abs(metric-np.mean(metric)) < 4 * np.std(metric)]



	path = 'Data\parameter_data_csv\p1+p2pow(x,p3).csv'
	
	names = ['job_00001', 'job_00014', 'job_00015', 'job_00054', 
			 'job_00120', 'job_00186', 'job_05926']
	omit = None
	# omit = ['job_04117']

	data, data_ = read_csv_(path, split_names=names, omit_names=omit)


	path = r'Data\amds\T2L_Energy_Density_AMDs1000_CLEAN.csv'
	# energy_data, _ = read_csv_(path, split_names=names, omit_names=omit, col_end=2)
	# data[:,2] = energy_data.T
	# data = np.flip(data, axis=0)

	# density_data, _ = read_csv_(path, split_names=names, omit_names=omit, col_start=2, col_end=3)
	# data[:,2] = density_data.T

	fig, ax = plt.subplots()
	labels = ['0001epsilon', '0014delta', '0015delta', '0054beta',
			  '0120gamma',   '0186alpha', '5926gamma']
	im = flatten_colour_label_scatter(data, ax, data_=data_, labels=labels)

	plt.xlabel('$a$')
	plt.ylabel('$b$')
	plt.title('$a+bx^p$')
	cbar = fig.colorbar(im, ax=ax)
	cbar.set_label('$p$')
	# plt.gca().set_aspect('equal', adjustable='box')
	plt.show()
