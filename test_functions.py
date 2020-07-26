import numpy as np
from scipy.optimize import curve_fit
import os

def my_root(x, root):
	return np.power(x, root)

def log_pow(x, param):
	return np.log(x) * np.power(x, param)

def n(x, param):
	a = x * param
	return np.sign(a) * (np.abs(a)) ** (0.35)

def my_rt(x, p1, p2, p3):
	# p4 = 1e-8 if p4 <= 0 else p4
	a = p2 + x * p3
	return p1 + np.sign(a) * (np.abs(a)) ** (1/3)

if __name__ == '__main__':
	filename = "T2L_Energy_Density_AMDs1000_CLEAN.csv"
	src = os.path.join("Data", filename)
	print(fancy_func(src))
