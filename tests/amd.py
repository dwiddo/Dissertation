import math
import numpy as np
from numpy.linalg import det
import matplotlib.pyplot as plt
import csv
import os
import ase.io
from scipy.optimize import curve_fit, minimize
import inspect

def approx(k, deter, n, t):
    num = 3 * (k) * deter
    denom = 4 * (math.pi) * (n/2)
    return (t * num / denom) ** (1./3.)

def fit_all_and_write_values(function_as_str, filepath):
    path_to_cifs = "Data/cifs/Large_T2_set/"
    errors = []
    names = []
    param_opts = []
    sigmas = []
    max_abs_diffs = []
    m_sizes = []

    # get AMDs
    src = "Data/amds/T2L_Energy_Density_AMDs1000_CLEAN.csv"
    with open(src) as f:
        reader = csv.reader(f)
        amds = []
        next(reader)
        for row in reader:
            amds.append([row[0]] + [float(x) for x in row[3:]])

    
    import progressbar
    for amd in progressbar.progressbar(amds):
        name = amd[0]
        file = name + '.cif'
        atoms = ase.io.read(path_to_cifs + file)
        # deter = det(atoms.get_cell())
        n = len(atoms.get_atomic_numbers())
        m_sizes.append(n)
        if n > 800:
            print(amd[0], n)
            plt.plot(amd[1:])
            plt.show()
    #     size = len(amd[1:])
    #     ydata = np.array(amd[1:], dtype=np.float64)
    #     xdata = np.linspace(1, size, size, dtype=np.float64)
            
    #     def approx_(k, t):
    #         return approx(k, deter, n, t)

    #     try:
    #         param_opt, _ = curve_fit(approx_, xdata, ydata, maxfev=10000000)
    #     except RuntimeError as e:
    #         print("runtime error:", str(e), "Skipping", name)
    #         continue
    #     names.append(name)
    #     param_opts.append(param_opt)
    #     errors.append(np.sqrt(np.sum(np.square(ydata - approx_(xdata, *param_opt))) / n))
    #     abs_diffs = np.absolute(ydata - approx_(xdata, *param_opt))
    #     sigmas.append(np.std(abs_diffs, ddof=1))
    #     max_abs_diffs.append(np.amax(abs_diffs))
    # av_err = sum(errors) / len(errors)
    # av_std = sum(sigmas) / len(sigmas)

    # with open(filepath + '.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     sig = list(inspect.signature(approx_).parameters.keys())[1:]
    #     writer.writerow(('name', *sig, '|M|', 'RMS', 'std_dev_abs_diff', 'max_abs_difference'))
    #     for name, params, m_size, err, sigma, max_diff in zip(names, param_opts, m_sizes, errors, sigmas, max_abs_diffs):
    #         writer.writerow((name, *params, m_size, err, sigma, max_diff))
    # with open(filepath + '.tag', 'w') as f:
    #     f.write("function:" + function_as_str + "\naverage_RMS:" + str(av_err) + "\naverage_std:" + str(av_std))

    # plt.hist([p[0] for p in param_opts])
    # plt.show()

if __name__ == '__main__':
    function_as_str = 'theoretical approximation'
    filepath = 'Data/parameter_data_csv/approx'
    fit_all_and_write_values(function_as_str, filepath)