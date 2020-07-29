import numpy as np
from scipy.optimize import curve_fit
import os

def my_rt(x, p1, p2):
	a = p1 * x
	return np.sign(a) * (np.abs(a)) ** p2

if __name__ == '__main__':
	filename = "T2L_Energy_Density_AMDs1000_CLEAN.csv"
	src = os.path.join("Data", filename)
	print(fancy_func(src))
