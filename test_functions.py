import numpy as np
from scipy.optimize import curve_fit
import os

def my_rt(x, p1):
	a = p1 * x
	return np.sign(a) * (np.abs(a)) ** 0.35076971

# def test(x, p):
# 	_a = p - 0.23949956 if p > 0.23949956 else 1
# 	a = 5.31243429 + 2.35809336 * np.log(_a)
# 	b = 0.07976559 + 0.06384552 / (p**3)
# 	return a + b * np.sign(x) * (np.abs(x)) ** p

if __name__ == '__main__':
	pass
