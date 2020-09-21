import numpy as np
from ccdc import io
import sys
sys.path.append('.')
import os
from ase.cell import Cell
from lib_tools.draw import draw
import csv
import re

def is_reduced(ase_cell):
    reduced_cell, op = ase_cell.niggli_reduce()
    post_op_cell = Cell.ascell((op.T @ ase_cell) @ op)
    
    if (np.allclose(post_op_cell.lengths(), reduced_cell.lengths()) and \
        np.allclose(post_op_cell.angles(), reduced_cell.angles())):
        return True, reduced_cell
    else:
        return False, reduced_cell

def COHN(formula):
    f = formula.split()
    if len(f) > 4:
        return False
    else:
        regex = re.compile('[^a-zA-Z]')
        for atoms in f:
            atom = regex.sub('', atoms)
            if atom not in ('C', 'O', 'H', 'N'):
                return False
        return True


"""
CSD with notable IDs. index, identifier:
142843 DEBXIT,   142844 DEBXIT01, 142845 DEBXIT02, 142846 DEBXIT03, 
142847 DEBXIT04, 142848 DEBXIT05, 142849 DEBXIT06
536326 NAVXUG
740213 SEMDIA
"""
if __name__ == '__main__':
    csd_crystal_reader = io.CrystalReader('CSD')
    # optionally add progress bar
    pbar = True
    if pbar:
        from progressbar import progressbar
        csd_crystal_reader = progressbar(csd_crystal_reader)

    no_unit_cell = 0
    no_motif     = 0
    no_formula   = 0

    with open('test.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['CSD_ID', 'cell_length_a', 'cell_length_b', 'cell_length_c',
                        'cell_angle_alpha', 'cell_angle_beta', 'cell_angle_gamma',
                        'is_reduced', 'crystal_system'])

        for crystal in csd_crystal_reader:
            cell_params = list(crystal.cell_lengths) + list(crystal.cell_angles)
            if not all(a == 0 for a in cell_params):
                # if COHN(crystal.formula):
                if crystal.formula:
                    if not len(crystal.molecule.atoms):
                        cell = Cell.new(cell_params)
                        is_red, reduced_cell = is_reduced(cell)
                        row = [crystal.identifier]
                        if is_red:
                            row.extend([*reduced_cell.lengths(), *reduced_cell.angles()])
                        else:
                            row.extend(cell_params)
                        row.append(is_red)
                        row.append(crystal.crystal_system)
                        writer.writerow(row)
                    else:
                        no_motif += 1
                else:
                    no_formula += 1 
            else:
                no_unit_cell += 1
    
    print("no unit cell:", no_unit_cell)
    print("no formula:", no_formula)
    print("no_motif:", no_motif)
            
