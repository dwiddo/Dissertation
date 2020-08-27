import numpy as np
from scipy.optimize import curve_fit
import os

def my_rt(x, p1, p2):
	return p1 * np.sign(x) * (np.abs(x) ** p2)

def f_(x, p1, p2, p3):
	return p1 + p2 * (np.sign(x) * (np.abs(x) ** p3))


def test(x, p):
	_a = max(1e-8, p - 0.22018971)
	a = 5.7890513 + 2.79125162 * np.log(_a)
	b = 0.40652574 + 0.01898218 * np.sign(p) * (np.abs(p) ** (-3.89713184))
	return a + b * np.sign(x) * ((np.abs(x)) ** p)

if __name__ == '__main__':
	pass
