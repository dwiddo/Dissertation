import os
from ase.io import read
import numpy as np
import networkx as nx
from scipy.spatial.distance import cdist
import time


def read_cif_files(directory, progress_bar=True):
    """
    yields atoms objects and filenames of all .cif files in directory
    :param directory: name of directory from which to read .cif files
    :param progress_bar: display a progressbar to the screen
    :yield: tuples (Atoms atoms, Str filename) read from directory
    use as follows;
    for atoms, filename in read_cif_files(dir):
        # code
    """
    if progress_bar:
        import progressbar
        files = progressbar.progressbar(os.listdir(directory))
    else:
        files = os.listdir(directory)

    for filename in files:
        if filename.endswith('.cif'):
            atoms = read(os.path.join(directory, filename))
            yield atoms, filename

def find_min_and_max(iterable, no_of_atoms=True, volume=True, no_of_components=False):
    """
    :param iterable: iterable of tuples (Atoms atoms, Str name) as given by read_cif_files()
    :param no_of_atoms: find max and min number of atoms in iterable
    :param volume: find max and min volume of unit cells of atoms in iterable
    :param no_of_components: find most and fewest connected components in iterable
    :returns: dict {'no_of_atoms': {'min':(Atoms atoms, Str name, Int no_of_atoms),'max':(...)}, ...}

    this function ignores ties. If two Atoms tie for anything, the one found first will be returned.
    """
    count = {
        'no_of_atoms': {'min': (None, None, float('inf')), 'max': (None, None, 0)},
        'volume': {'min': (None, None, float('inf')), 'max': (None, None, 0)},
        'no_of_components': {'min': (None, None, float('inf')), 'max': (None, None, 0)}
    }

    for atoms, name in iterable:
        if no_of_atoms:
            no_atoms = len(atoms)
            if no_atoms > count['no_of_atoms']['max'][2]:
                count['no_of_atoms']['max'] = (atoms, name, no_atoms)
            elif no_atoms < count['no_of_atoms']['min'][2]:
                count['no_of_atoms']['min'] = (atoms, name, no_atoms)
        if volume:
            vol = atoms.get_volume()
            if vol > count['volume']['max'][2]:
                count['volume']['max'] = (atoms, name, vol)
            elif vol < count['volume']['min'][2]:
                count['volume']['min'] = (atoms, name, vol)
        if no_of_components:
            atoms = unwrap_atoms_from_cell(atoms)
            components = len(get_connected_components(atoms.get_positions(), atoms.get_chemical_symbols()))
            if components > count['no_of_components']['max'][2]:
                count['no_of_components']['max'] = (atoms, name, components)
            elif components < count['no_of_components']['min'][2]:
                count['no_of_components']['min'] = (atoms, name, components)

    return count

def find_bonds(p1, s1, p2=None, s2=None, bool=False):
    """
    find possible chemical bonds between atoms in p1 and p2 (lists of positions).
    s1 and s2 are list of the chemical symbols of the atoms. If bool, then returns
    True as soon as any bond is found, otherwise get and return all bonds found.
    :param p1: np array of atoms positions (acceptable from ase.Atoms.get_positions())
    :param s1: list of p1's chemical symbols
    :param p2: optional np array of positions. if given only find bonds between p1 and p2
    :param s2: optional list of p2's symbols
    :param bool: if True, return any bond if found otherwise return False. if False, return list of bonds found.
    :return: list of tuples [(i,j),...] where i and j are indices of bonded atoms.
    """
    if p2 is None or s2 is None:
        s2 = s1
        p2 = p1
    bond_radii = {
        "H":  0.23,
        "C":  0.68,
        "N":  0.68,
        "O":  0.68,
        # "P":  0.75,
        # "S":  1.02
    }

    max_bond_len = 2 * max(bond_radii.values()) + 0.45
    bonds = []
    distances = np.array(cdist(p1,p2))
    mask = (distances > 0) & (distances < max_bond_len)
    for i, row in enumerate(mask):
        if np.any(row[i+1:]):
            b1 = bond_radii[s1[i]] + 0.45
            for j, x in enumerate(row[i+1:]):
                if x:
                    ind = j+i+1
                    accepted_radius = b1 + bond_radii[s2[ind]]
                    if distances[i, ind] < accepted_radius:
                        if bool:
                            return (i, ind)
                        bonds.append((i,ind))
    if bool:
        return False
    return bonds

def get_connected_components(positions, symbols):
    """
    :return: list of np arrays containing indices of connected components.
    """
    bonds = find_bonds(positions, symbols)
    graph = nx.Graph()
    graph.add_nodes_from(range(len(positions)))
    graph.add_edges_from(bonds)
    components = [np.array(list(c)) for c in nx.connected_components(graph)]
    return components

def get_component_centers(atoms, unwrap=False):
    """
    get center of mass of each connected component of the atoms object.
    """
    if unwrap:
        atoms = unwrap_atoms_from_cell(atoms)
    pos = atoms.get_positions()
    masses = atoms.get_masses()
    components = get_connected_components(pos, atoms.get_chemical_symbols())
    centers = []
    for c in components:
        centers.append(np.dot(masses[c], pos[c]) / masses[c].sum())
    return np.array(centers)

def unwrap_atoms_from_cell(atoms, wrap_centers_into_cell=False):
    """
    :param atoms: Atoms object to unwrap
    :return: 'unwrapped' Atoms object, with atomic positions moved to more 'natural' positions outside
            the unit cell (finding where there are chemical bonds chopped by wrapping into the cell)
    This gives wholly connected molecules instead of having some atoms wrapped inside the unit cell.
    """
    # collection of possible directions to translate by
    c = atoms.get_cell()
    directions = [c[0],c[1],c[2],
                c[0]+c[1],c[0]-c[1],c[0]+c[2],c[0]-c[2],c[1]+c[2],c[1]-c[2],
                c[0]+c[1]+c[2],c[0]+c[1]-c[2],c[0]-c[1]+c[2],c[0]-c[1]-c[2]]
    directions = [val for pair in zip(directions, [-x for x in directions]) for val in pair]
    symbols = np.char.array(atoms.get_chemical_symbols())
    positions = atoms.get_positions()
    # do until no more components get connected
    have_joined_components = True
    components = get_connected_components(positions, symbols)
    while have_joined_components:
        components.sort(key=len)
        max_component_size = len(components[-1])
        have_joined_components = False
        for component in components:
            if len(component) == max_component_size:
                break
            component_position = positions[component]
            s1 = symbols[component]
            all_other_atoms = [i for c in components for i in c if c is not component]
            p2 = positions[all_other_atoms]
            s2 = symbols[all_other_atoms]
            for direction in directions:
                p1 = [p + direction for p in component_position]
                new_bond = find_bonds(p1, s1, p2, s2, bool=True)
                # if a bond was found, translate the component
                if new_bond:
                    # for atom in component:
                    #     positions[atom] += direction
                    positions[component] += direction
                    a = component[new_bond[0]]
                    b = all_other_atoms[new_bond[1]]
                    new_components = []
                    for c in components:
                        if c is not component:
                            if b not in c:
                                new_components.append(c)
                            else:
                                component_ = c
                    new_components.append(np.concatenate((component, component_)))
                    components = new_components
                    have_joined_components = True
                    break
            if have_joined_components:
                break
    atoms.set_positions(positions, apply_constraint=False)
    if wrap_centers_into_cell:
        cell = atoms.get_cell()
        cart_to_fract = np.linalg.inv(cell.array)
        centers = get_component_centers(atoms)
        components = get_connected_components(atoms.get_positions(), atoms.get_chemical_symbols())
        scaled_centers = np.matmul(centers, cart_to_fract)
        cell_lengths = atoms.get_cell_lengths_and_angles()
        for i, c in enumerate(scaled_centers):
            for j, coord in enumerate(c):
                if coord < 0:
                    for atom in components[i]:
                        positions[atom] += cell[j]
                elif coord > 1:
                    for atom in components[i]:
                        positions[atom] -= cell[j]

        atoms.set_positions(positions, apply_constraint=False)

    return atoms

def unwrap(atoms):
    from ase import neighborlist
    from scipy import sparse
    import networkx as nx
    cutoff = neighborlist.natural_cutoffs(atoms)
    bonds = neighborlist.neighbor_list('ijS', atoms, cutoff)
    atoms.pbc = [False, False, False]
    nl = neighborlist.build_neighbor_list(atoms)
    nl.update(atoms)
    matrix = nl.get_connectivity_matrix(sparse=False)
    g = nx.from_numpy_matrix(matrix)
    components = [np.array(list(c)) for c in nx.connected_components(g)]
    components.sort(key=len)
    positions = atoms.get_positions()
    joining = True
    count = 0
    moved = []
    while joining:
        count += 1
        if count > 10:
            print("retn")
            atoms.set_positions(positions, apply_constraint=False)
            return atoms
        joining = False
        for c in components:
            print(components)
            if len(c) == len(components[-1]):
                break
            for atom in c:
                # a is list of indexes for bonds of atom
                a = np.array([i for i, x in enumerate(bonds[0]) if x == atom])
                print("comp",c)
                print("atom",atom)
                print("b0",bonds[0])
                print("b1",bonds[1])
                print("a",a)
                if len(a) == 0:
                    print("no bonds found!")
                    continue
                for i, v in enumerate(bonds[2][a]):
                    if np.any(v):
                        adjacent_atom = bonds[1][a][i]
                        if adjacent_atom in c \
                            or (atom, adjacent_atom) in moved \
                            or (adjacent_atom, atom) in moved:
                            continue
                        match = [s for s in components if adjacent_atom in s]
                        components = [s for s in components if adjacent_atom not in s]
                        del components[0]
                        components.append(np.concatenate((match[0], c)))
                        components.sort(key=len)
                        print("c",c)
                        print("adj",adjacent_atom)
                        print("m",match)
                        print("v",v)
                        positions[c] -= v.dot(atoms.cell)
                        moved.append((atom, adjacent_atom))
                        joining = True
                        break
            if joining:
                break
    atoms.set_positions(positions, apply_constraint=False)
    return atoms

def compare_centers(atoms, eps=np.float32(1e-3)):
    positions = atoms.get_positions()
    cell = atoms.get_cell()
    cart_to_fract = np.linalg.inv(cell.array)   # change of basis matrix
    centers = get_component_centers(atoms, unwrap=True)
    scaled_centers = np.matmul(centers, cart_to_fract)
    pairs = []
    for i, c in enumerate(scaled_centers):
        for j, c_ in enumerate(scaled_centers[i+1:]):
            x = np.absolute(c_ - c)
            if np.any(x < eps):
                print(x)
                pairs.append((centers[i], centers[i+j+1]))
    return pairs

if __name__ == "__main__":

    import warnings
    warnings.filterwarnings("ignore")
    CIF_DIRECTORY = "CIFs/"
    # "job_03351.cif" simplest crystal
    # "job_06871.cif" largest volume
    # "job_06467.cif" most atoms
    # atoms = read(os.path.join(CIF_DIRECTORY, "job_03351.cif"))
    import ase_plotter
    import matplotlib.pyplot as plt
    import progressbar
    n = 500
    t = 0
    atoms = read(os.path.join(CIF_DIRECTORY, "job_03351.cif"))
    # unwrap_atoms_from_cell(atoms)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ase_plotter.draw(atoms, ax, draw_centers=False)
    plt.show()
