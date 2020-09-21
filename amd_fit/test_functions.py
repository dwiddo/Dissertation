import numpy as np
from scipy.optimize import curve_fit
import os

def my_rt(x, p1, p2):
	return p1 * np.sign(x) * (np.abs(x) ** p2)

def f_(x, p1, p2, p3):
	return p1 + p2 * (np.sign(x) * (np.abs(x) ** p3))

def f__(x, a, b, c, d, p):
	t = x + d
	t[t<0] = 1e-8
	return a + b * x ** p + c * np.log(t)

def new_idea(x, a, b, c, d, p):
	t = c*x + d
	return a + b * np.sign(t) * (np.abs(t) ** p)

if __name__ == '__main__':
	pass
