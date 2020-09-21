from scipy.optimize import curve_fit
import numpy as np
import csv
import matplotlib.pyplot as plt






# plots some random amd curves
"""
plt.rcParams.update({'font.size': 20})

path = r"Data\amds\T2L_Energy_Density_AMDs1000_CLEAN.csv"
spacing = 500
with open(path) as f:
    reader = csv.reader(f)
    next(reader)
    for _ in range(6):
        for _ in range(470):
            line = next(reader)
        data = [float(x) for x in line[3:]]
        plt.plot(data, linewidth=4)

plt.xlabel('$k$')
plt.ylabel('AMD$_k$')
plt.show()
"""