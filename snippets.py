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

def flatten_colour_label_scatter(data, ax, data_=None, data__labels=None):
	"""
	:param: data 
		np array of shape (n,3)
	:param: ax
		matplotlib axes object to draw to
	:param: data_
		np array of shape (n,3)
	:param: data__labels
		container of strings the same length as data_ (len(lata__labels) == data.shape[0])
		
	:return:
		matplotlib PathCollection object returned from scatter. Useful to add colourbar.

	plot first two columns of data as a scatter to ax, and colour based on the third.
	points in data_ will be labelled with data__labels and coloured black.
	"""

	X = data[:,2]
	Y = data[:,0]
	clr = data[:,1]

	im = ax.scatter(X, Y, s=3, c=clr, cmap='seismic',
				norm=colors.PowerNorm(gamma=0.5)
				# norm=colors.LogNorm(vmin=clr.min(), vmax=clr.max())
				)
	if data_ is not None:
		X_ = data_[:,2]
		Y_ = data_[:,0]
		ax.scatter(X_, Y_, s=4, c='k')
		# arrived at offsets manually
		offsets = [(-50,-10), (3,0), (-55,0), (-20,-12), (3,0), (3,0), (3,0)]
		for i, name in enumerate(data__labels):
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
	
	highlight = ['job_00001', 'job_00014', 'job_00015', 'job_00054', 'job_00120', 'job_00186', 'job_05926']
	# omit_names = None
	omit = ['job_04117']

	data, data_ = read_csv_(path, split_names=highlight, omit_names=omit)
	fig, ax = plt.subplots()
	im = flatten_colour_label_scatter(data, ax, data_=data_, data__labels=highlight)

	data, _ = read_csv_(path, omit_names=omit)
	# p = np.polyfit(data[:,0], data[:,1], 1)
	## >>> [-0.54336499  1.66794143]
	# x = np.linspace(-6, 5, 1000)
	# y = p[0] * x + p[1]
	# plt.plot(x, y)

	from scipy.optimize import curve_fit

	def function(p, p1, p2, p3):
		return np.log(p1 + p) * p2 + p3

	param_opt, _ = curve_fit(function, data[:,2], data[:,0])
	print(param_opt)
	# >>> [0.06384552 0.07976559] for b(p) = p1 / p**3 + p2
	# >>> [-0.23949956  2.35809336  5.31243429] for a(p) = log(p1 + p) * p2 + p3
	x = np.linspace(0.245, 0.7, 1000)
	y = function(x, *param_opt)
	plt.plot(x,y)

	plt.xlabel('a')
	plt.ylabel('b')
	plt.title("a+b*x^p")
	cbar = fig.colorbar(im, ax=ax)
	cbar.set_label("p")
	# plt.gca().set_aspect('equal', adjustable='box')
	plt.show()
	