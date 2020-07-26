import ase_utils
import os
from ase.io import read
import numpy as np
import matplotlib.pyplot as plt

def draw_line(p1, p2, ax, linewidth=1, linestyle='solid'):
    """
    draw line on ax from p1 to p2 (cartesian vectors).
    :param p1: (x,y,z) carteisan vector
    :param p2: (x,y,z) carteisan vector
    :param ax: pyplot 3D Plot object to draw to
    :param linewidth: line thickness
    """
    x = np.linspace(p1[0], p2[0], 100)
    y = np.linspace(p1[1], p2[1], 100)
    z = np.linspace(p1[2], p2[2], 100)
    ax.plot(x, y, z, c='k', linewidth=linewidth, linestyle=linestyle)

def draw_cell(cell, ax):
    """
    draw ase.cell.Cell object to ax.
    """
    for vector in cell:
        draw_line([0,0,0], vector, ax)
    # get corners.
    c1 = cell[0] + cell[1]
    c2 = cell[0] + cell[2]
    c3 = cell[1] + cell[2]
    c4 = cell[0] + cell[1] + cell[2]
    for i, corner in enumerate([c1,c3,c2]):
    	draw_line(corner, cell[i%3], ax)
    	draw_line(corner, cell[(i+1)%3], ax)
    	draw_line(corner, c4, ax)

def draw(atoms, ax, draw_atoms=True,
                    draw_bonds=True,
                    draw_unit_cell=True,
                    draw_centers=False,
                    unwrap=True):
    """
    update func
    :param atoms: Atoms object or str of a .cif filename.
    draw atoms object to ax. Optionally draw chemical bonds, unit cell, or unwrap atoms
    from the unit cell (see unwrap_atoms_from_cell() for explanation of unwrapping).
    """
    if isinstance(atoms, str):
    	atoms = read(atoms)

    if draw_unit_cell: draw_cell(atoms.get_cell(), ax)

    if unwrap: atoms = ase_utils.unwrap_atoms_from_cell(atoms)
    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()

    if draw_centers:
        points = ase_utils.get_component_centers(atoms)
        ax.scatter(points[:,0], points[:,1], points[:,2], s=70)

    if draw_bonds:
        if atoms.has('tags'):
            tags = atoms.get_array('tags')
            occ  = atoms.info['occupancy']
        else:
            tags = None
        bonds = ase_utils.find_bonds(positions, symbols)
        for bond in bonds:
            linestyle = 'solid'
            position  = positions[bond[0]]
            position_ = positions[bond[1]]
            if tags is not None:
                i  = tags[bond[0]]
                i_ = tags[bond[1]]
                o  = occ[i][symbols[bond[0]]]
                o_ = occ[i_][symbols[bond[1]]]
                if o < 1 and o_ < 1:
                    linestyle= 'dashed'

            draw_line(position, position_, ax, linewidth=2, linestyle=linestyle)
    if draw_atoms:
        colours = {
            "H":  '#B8B8B8',
            "C":  "#585858",
            "N":  'c',
            "O":  'r',
            "P":  'm',
            "S":  'g'
        }
        colour_list = [colours[s] for s in np.char.array(symbols)]
        ax.scatter(positions[:,0], positions[:,1], positions[:,2], c=colour_list, s=30, alpha=1)

def draw_each_component(atoms, draw_atoms=True,
                        draw_bonds=True,
                        draw_unit_cell=True,
                        unwrap=True):

    if isinstance(atoms, str):
        atoms = read(atoms)
    if unwrap: atoms = ase_utils.unwrap_atoms_from_cell(atoms)
    symbols = atoms.get_chemical_symbols()
    positions = atoms.get_positions()
    components = ase_utils.get_connected_components(positions, symbols)

    for component in components:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        if draw_unit_cell: draw_cell(atoms.get_cell(), ax)

        if draw_bonds:
            if atoms.has('tags'):
                tags = atoms.get_array('tags')
                occ  = atoms.info['occupancy']
            else:
                tags = None
            bonds = ase_utils.find_bonds(positions, symbols)
            for bond in bonds:
                if bond[0] in component and bond[1] in component:
                    linestyle = 'solid'
                    position  = positions[bond[0]]
                    position_ = positions[bond[1]]
                    if tags is not None:
                        i  = tags[bond[0]]
                        i_ = tags[bond[1]]
                        o  = occ[i][symbols[bond[0]]]
                        o_ = occ[i_][symbols[bond[1]]]
                        if o < 1 and o_ < 1:
                            linestyle= 'dashed'

                    draw_line(position, position_, ax,
                        linewidth=2, linestyle=linestyle)

        if draw_atoms:
            colours = {
                "H":  '#B8B8B8',
                "C":  '#585858',
                "N":  'c',
                "O":  'r',
                "P":  'm',
                "S":  'g'
            }
            colour_list = [colours[s] for i,s in enumerate(symbols) if i in component]
            ax.scatter(positions[:,0][component],
                positions[:,1][component],
                positions[:,2][component],
                c=colour_list, s=90, alpha=1)
        plt.show()
        plt.close()


"""
EXPERIMENTS
"""

# def draw_abstract_structure(atoms, ax, draw_unit_cell=True, draw_centers=True):
#     if isinstance(atoms, str):
#         atoms = read(atoms)

#     if draw_unit_cell: draw_cell(atoms.get_cell(), ax)

#     if draw_centers:
#         points = np.array(ase_utils.get_component_centers(atoms))
#         ax.scatter(points[:,0], points[:,1], points[:,2], s=70)

def draw_aligned_centers(atoms, ax):
    positions = atoms.get_positions()
    links = ase_utils.compare_centers(atoms)
    for link in links:
        draw_line(link[0], link[1], ax, linewidth=2)

def draw_normals(atoms, ax):
    atoms = ase_utils.unwrap_atoms_from_cell(atoms)
    positions = atoms.get_positions()
    components = ase_utils.get_connected_components(positions, atoms.get_chemical_symbols())
    centers = ase_utils.get_component_centers(atoms)
    for i, component in enumerate(components):
        points = positions[component]
        points = np.transpose(points)
        points = np.transpose(np.transpose(points) - np.sum(points,1) / len(np.transpose(points))) # subtract out the centroid
        svd = np.transpose(np.linalg.svd(points)) # singular value decomposition
        normal = np.transpose(svd[0])[2]
        draw_line(centers[i], centers[i] + normal, ax, linewidth=2)

if __name__ == "__main__":
    # import warnings
    # warnings.filterwarnings("ignore")
    CIF_DIRECTORY = "cifs/Large_T2_set/"
    # "job_03351.cif" simplest crystal
    # "job_06871.cif" largest volume
    # "job_06467.cif" most atoms
    atoms = read(os.path.join(CIF_DIRECTORY, "job_03154.cif"),
                fractional_occupancies=True)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    draw(atoms, ax, draw_centers=True)
    plt.show()
    # # atoms.edit()
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # draw(atoms, ax, draw_centers=False)
    # # draw_aligned_centers(atoms, ax)
    # # draw_normals(atoms, ax)
    # ax.set_xlabel("x")
    # ax.set_ylabel("y")
    # ax.set_zlabel("z")
    # plt.show()
    # plt.close()

    # no = []
    # picks = {}
    # for atoms, filename in ase_utils.read_cif_files(CIF_DIRECTORY):
    #     atoms = ase_utils.unwrap_atoms_from_cell(atoms)
    #     p = atoms.get_positions()
    #     s = atoms.get_chemical_symbols()
    #     l = len(ase_utils.get_connected_components(p, s))
    #     if l == 3 or l == 5 or l == 9 or l == 13 or l == 10 or l == 18 or l == 32:
    #         print(filename, "has", l, "components")
    #         picks[filename] = l
    #     no.append(l)

    # from collections import Counter
    # print(Counter(sorted(no)))
    # print(picks)
    # a = plt.hist(no, bins=np.arange(min(no), max(no) + 1, 1))
    # plt.show()

# Counter({8: 2201, 4: 1329, 6: 643, 12: 633, 16: 543, 2: 226, 24: 49, 36: 20, 3: 14, 5: 10, 9: 3, 13: 3, 10: 2, 1: 1, 18: 1, 32: 1})
# {'job_00254.cif': 5, 'job_00383.cif': 3, 'job_00573.cif': 10, 'job_00680.cif': 5, 'job_01243.cif': 3, 'job_01577.cif': 3, 'job_01649.cif': 5,
# 'job_01752.cif': 5, 'job_02188.cif': 5, 'job_02675.cif': 3, 'job_03094.cif': 3, 'job_03135.cif': 5, 'job_03250.cif': 32, 'job_03869.cif': 5,
# 'job_04004.cif': 10, 'job_04109.cif': 3, 'job_04907.cif': 5, 'job_05188.cif': 9, 'job_05275.cif': 3, 'job_05453.cif': 3, 'job_05466.cif': 3,
# 'job_05475.cif': 5, 'job_05658.cif': 3, 'job_05677.cif': 3, 'job_05710.cif': 3, 'job_05786.cif': 3, 'job_05805.cif': 3, 'job_05860.cif': 5,
# 'job_05908.cif': 9, 'job_05909.cif': 9, 'job_06315.cif': 18, 'job_06633.cif': 13, 'job_06771.cif': 13, 'job_06956.cif': 13}
