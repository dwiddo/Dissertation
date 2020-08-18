import numpy as np
from ccdc import io
import sys
sys.path.append('.')
import os
from ase.cell import Cell
from lib_tools.draw import draw
import csv

"""
CSD with notable IDs. index, identifier:
142843 DEBXIT,   142844 DEBXIT01, 142845 DEBXIT02, 142846 DEBXIT03, 
142847 DEBXIT04, 142848 DEBXIT05, 142849 DEBXIT06
536326 NAVXUG
740213 SEMDIA
"""

def is_reduced(ase_cell):
    reduced_cell, op = ase_cell.niggli_reduce()
    post_op_cell = Cell.ascell((op.T @ ase_cell) @ op)

    if (np.allclose(post_op_cell.lengths(), reduced_cell.lengths()) and \
        np.allclose(post_op_cell.angles(), reduced_cell.angles())):
        return True, reduced_cell
    else:
        return False, reduced_cell

# # testing csd reduced cells against ase reduced cells
# csd_crystal_reader = io.CrystalReader('CSD')
# for i, crystal in enumerate(csd_crystal_reader):
#     cell_params = list(crystal.cell_lengths) + list(crystal.cell_angles)
#     if not all(a == 0 for a in cell_params):
#         _, ase_reduced = is_reduced(Cell.new(cell_params))
#         try:
#             csd_reduced_l = np.array(crystal.reduced_cell.cell_lengths)
#             csd_reduced_a = np.array(crystal.reduced_cell.cell_angles)
#             if not (np.allclose(ase_reduced.lengths(), csd_reduced_l) and \
#                     np.allclose(ase_reduced.angles(), csd_reduced_a)):
#                 print('Mismatch at index='+str(i), 'ID='+crystal.identifier)
#                 print('raw parameters:', np.array(crystal.cell_lengths), np.array(crystal.cell_angles))
#                 print('ase parameters:', ase_reduced.lengths(), ase_reduced.angles())
#                 print('csd parameters:', csd_reduced_l, csd_reduced_a)
#         except:
#             pass
#     if i > 500:
#         exit()


# # write & draw crystal using index
# csd_crystal_reader = io.CrystalReader('CSD')
# crystal = csd_crystal_reader[3021]
# writepath = crystal.identifier + '.cif'
# with io.CrystalWriter(writepath) as writer:
#     writer.write(crystal)
# draw(writepath)