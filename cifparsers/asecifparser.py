import ase.io

# path to cif
cif_path = 'cifparsers/job_00001.cif'
atoms = ase.io.read(cif_path)   # create ase.Atoms object from cif

atoms.get_cell()                        # cartesian cell (acts as 3x3 ndarray)
atoms.get_cell_lengths_and_angles()     # cell parameters
atoms.get_atomic_numbers()              # array of atomic numbers
atoms.get_positions()                   # positions of atoms (cartesian)
atoms.get_scaled_positions()            # positions of atoms (fractional)
# etc, etc. see docs or help file for more
# or get a list of all methods/properties with:
# print(dir(atoms))


