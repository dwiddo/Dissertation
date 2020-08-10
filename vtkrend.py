import vtkplotlib as vpl
import numpy as np
import csv
import os
import matplotlib.pyplot as plt


filename = "p1+p2pow(x,p3).csv"
src = os.path.join("Data/new", filename)

data = []
with open(src) as f:
    reader = csv.reader(f)
    next(reader)
    next(reader)
    for line in reader:
        data.append([float(x) for x in line[1:4]])

data = np.array(data)
print(data.shape)
# fig = plt.figure()
# vpl.scatter(data, radius=0.1)
# vpl.show()

# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(data[:,0],data[:,1],data[:,2])
# ax.set_xlabel("p1")
# ax.set_ylabel("p2")
# ax.set_zlabel("p3")
# plt.show()

from uvw import RectilinearGrid, DataArray, StructuredGrid
import uvw

# x = np.linspace(-0.5, 0.5, 10)
# y = np.linspace(-0.5, 0.5, 20)
# z = np.linspace(-0.9, 0.9, 30)

# Creating the file (with possible data compression)
grid = StructuredGrid('grid.vtk', data, range(3))

# A centered ball
# x, y, z = np.meshgrid(x, y, z, indexing='ij')
# r = np.sqrt(x**2 + y**2 + z**2)
# ball = r < 0.3
#
# # Some multi-component multi-dimensional data
# data = np.zeros([10, 20, 30, 3, 3])
# data[ball, ...] = np.array([[0, 1, 0],
#                             [1, 0, 0],
#                             [0, 1, 1]])
#
# # Some cell data
# cell_data = np.zeros([9, 19, 29])
# cell_data[0::2, 0::2, 0::2] = 1

# Adding the point data (see help(DataArray) for more info)
grid.addPointData(DataArray(data, range(3), 'ball'))
# Adding the cell data
# grid.addCellData(DataArray(cell_data, range(3), 'checkers'))
grid.write()
