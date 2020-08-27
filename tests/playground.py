from scipy.optimize import curve_fit
import numpy as np
import csv


def pa(p, p1, p2, p3):
    return p1 + p2 * np.sign(p) * (np.abs(p) ** (p3))

def pb(p, p1, p2, p3):
    return p1 + p2 * np.sign(p) * (np.abs(p) ** (-p3))

path = r'Data\parameter_data_csv\p1+p2pow(x,p3).csv'

params = []
with open(path) as file:
    reader = csv.reader(file)
    next(reader)
    for line in reader:
        params.append([float(x) for x in line[1:4]])

params = np.array(params)
print(params)

param_opt, _ = curve_fit(pa, params[:,2], params[:,0], maxfev=500000)

print(param_opt)
# a(p) = 
# b(p) = 0.40652574 + 0.01898218 * p ^ (-3.89713184)
