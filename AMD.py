import csv
from scipy.optimize import curve_fit, minimize
import numpy as np
import matplotlib.pyplot as plt
import os
import inspect

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
				param_opt, _ = curve_fit(function, xdata, ydata, maxfev=1000000)
			except RuntimeError:
				print("runtime error...")
				continue
			param_opts.append(param_opt)
			errors.append(np.sum(np.square(ydata - function(xdata, *param_opt))) / n)
	arg_max = np.argmax(errors)
	arg_min = np.argmin(errors)
	av_err  = sum(errors) / len(errors)
	min_max_dict = {names[arg_min] : errors[arg_min], names[arg_max] : errors[arg_max]}
	return param_opts
	# return min_max_dict, av_err

def fit_all_and_write_values(src, function, function_as_str, filepath):
	errors = []
	names = []
	param_opts = []
	with open(src) as f:
		reader = csv.reader(f)
		next(reader)
		import progressbar
		for line in progressbar.progressbar(reader):
			y = [float(i) for i in line[3:]]
			n = len(y)
			xdata = np.linspace(1, n, n)
			ydata = np.array(y, dtype=np.float64)
			try:
				param_opt, _ = curve_fit(function, xdata, ydata, maxfev=1000000)
			except RuntimeError:
				print("runtime error... skipping", line[0])
				continue
			names.append(line[0])
			param_opts.append(param_opt)
			errors.append(np.sum(np.square(ydata - function(xdata, *param_opt))) / n)
	av_err  = sum(errors) / len(errors)
	with open(filepath, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(("function:" + function_as_str, "average_MSE:" + str(av_err)))
		sig = list(inspect.signature(function).parameters.keys())[1:]
		writer.writerow(('name', *sig, 'MSE'))
		for name, params, err in zip(names, param_opts, errors):
			writer.writerow((name, *params, err))

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

	def outer_f(const):
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
	s = "(p1*x)^p2"
	filepath = "Data/pow(p1x,p2).csv"
	# d = fit_all_and_write_values(src, my_rt, s, filepath)
	params = fit_all(src, my_rt)
	for i in range(len(params[0])):
		plt.hist([p[i] for p in params], bins=250)
		plt.show()
