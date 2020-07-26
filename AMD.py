import csv
from scipy.optimize import curve_fit, minimize
import numpy as np
import matplotlib.pyplot as plt
import os

"""
Some experimental functions for fitting the AMD curves.
"""

def fit_all(src, function):
	errors = []
	names = []
	param_opts = []
	with open(src) as f:
		reader = csv.reader(f)
		next(reader)
		import progressbar
		for line in progressbar.progressbar(reader):
			names.append(line[0])
			y = [float(i) for i in line[3:]]
			n = len(y)
			xdata = np.linspace(1, n, n)
			ydata = np.array(y, dtype=np.float64)
			try:
				param_opt, _ = curve_fit(function, xdata, ydata, maxfev=10000000, )#p0=[-1, 1, 1, 1/3])
			except RuntimeError:
				print("runtime error...")
				continue
			param_opts.append(param_opt)
			errors.append(np.sum(np.square(ydata - function(xdata, *param_opt))) / n)
	arg_max = np.argmax(errors)
	arg_min = np.argmin(errors)
	av_err  = sum(errors) / len(errors)
	min_max_dict = {names[arg_min] : errors[arg_min], names[arg_max] : errors[arg_max]}
	for i, p in enumerate(param_opts):
		if any(j >= 100 or j <= 100 for j in p):
			print(names[i], p)
	# print(np.sort(np.array(param_opts)))
	print(np.average(np.array(param_opts), axis=0))
	return min_max_dict, av_err


def fit_all_and_consts(src, function):
	errors = []
	names = []
	with open(src) as f:
		reader = csv.reader(f)
		next(reader)
		import progressbar
		for line in progressbar.progressbar(reader):
			names.append(line[0])
			y = [float(i) for i in line[3:]]
			n = len(y)
			xdata = np.linspace(1, n, n)
			ydata = np.array(y, dtype=np.float64)
			param_opt, _ = curve_fit(function, xdata, ydata)
			errors.append(np.sum(np.square(ydata - function(xdata, *param_opt))) / n)
	arg_max = np.argmax(errors)
	arg_min = np.argmin(errors)
	av_err  = sum(errors) / len(errors)
	min_max_dict = {names[arg_min] : errors[arg_min], names[arg_max] : errors[arg_max]}
	return min_max_dict, av_err

def plot_one_actual_and_fitted(src, function, job_name):
	with open(src) as f:
		reader = csv.reader(f)
		next(reader)
		for line in reader:
			if line[0] == job_name:
				y = [float(i) for i in line[3:]]
				n = len(y)
				xdata = np.linspace(1, n, n)
				ydata = np.array(y, dtype=np.float64)
				param_opt, _ = curve_fit(function, xdata, ydata)
				plt.plot(ydata, label='actual')
				plt.plot(function(xdata, *param_opt), label='fitted')
				plt.legend()
				plt.show()
				plt.close()
				break

def plot_all_actual_and_fitted(src, function):
	with open(src) as f:
		reader = csv.reader(f)
		next(reader)
		for line in reader:
			y = [float(i) for i in line[3:]]
			n = len(y)
			xdata = np.linspace(1, n, n)
			ydata = np.array(y, dtype=np.float64)
			param_opt, _ = curve_fit(function, xdata, ydata)
			plt.plot(ydata, label='actual')
			plt.plot(function(xdata, *param_opt), label='fitted')
			plt.legend()
			plt.show()
			plt.close()

def plot_est_derivative(src, job_name):
	with open(src) as f:
		reader = csv.reader(f)
		next(reader)
		for line in reader:
			if line[0] == job_name:
				y = [float(i) for i in line[3:]]
				diffs = np.array(y[1:]) - np.array(y[:-1])
				plt.plot(diffs)
				print(diffs)
				plt.show()
				plt.close()
				break

def find_const(src):
	import csv
	amds = []
	with open(src) as f:
		reader = csv.reader(f)
		next(reader)
		for line in reader:
			amds.append([float(i) for i in line[3:]])
	amds = np.array(amds, dtype=np.float64)
	n = amds.shape[1]
	xdata = np.linspace(1, n, n)

	# import progressbar
	def outer_f(const):
		# def f(x, p1, p2, p3):
		# 	a = p2 + p1 * x
		# 	return p3 + np.sign(a) * (np.abs(a)) ** const
		def f(x, p1):
			a = p1 * x
			return np.sign(a) * (np.abs(a)) ** const
		e = []
		for amd in amds:
			param_opt, _ = curve_fit(f, xdata, amd)
			e.append(np.sum(np.square(amd - f(xdata, *param_opt))) / n)
		av_err = sum(e) / len(e)
		print("c:", const, "e:", av_err)
		return av_err

	return minimize(outer_f, 0.35)

def plot_errors(src, range):
	import csv
	amds = []
	with open(src) as f:
		reader = csv.reader(f)
		next(reader)
		for line in reader:
			amds.append([float(i) for i in line[3:]])
	amds = np.array(amds, dtype=np.float64)
	n = amds.shape[1]
	xdata = np.linspace(1, n, n)

	def outer_f(const):
		def f(x, p1):
			a = p1 * x
			return const + np.sign(a) * (np.abs(a)) ** (1/3)
		e = []
		for amd in amds:
			param_opt, _ = curve_fit(f, xdata, amd)
			e.append(np.sum(np.square(amd - f(xdata, *param_opt))) / n)
		av_err = sum(e) / len(e)
		# print("c:", const, "e:", av_err)
		return av_err
	errors = []
	constants = np.linspace(range[0], range[1], 20)
	import progressbar
	for const in progressbar.progressbar(constants):
		errors.append(outer_f(const))

	plt.plot(constants, errors)
	plt.show()

if __name__ == '__main__':
	from test_functions import my_rt
	filename = "T2L_Energy_Density_AMDs1000_CLEAN.csv"
	src = os.path.join("Data", filename)
	# plot_all_actual_and_fitted(src, test_functions.my_rt)
	# plot_one_actual_and_fitted(src, test_functions.my_rt, "job_00721")
	d = fit_all(src, my_rt)
	print(d)
	# print(find_const(src))
