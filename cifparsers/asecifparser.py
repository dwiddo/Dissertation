import ase.io

# path to cif
cif_path = 'cifparsers/job_00001.cif'
atoms = ase.io.read(cif_path)   # create ase.Atoms object from cif

atoms.get_cell()                        # cartesian cell (acts as 3x3 ndarray)
atoms.get_cell().niggli_reduce()        # niggli reduce the cell
atoms.get_cell_lengths_and_angles()     # cell parameters
atoms.get_atomic_numbers()              # array of atomic numbers
atoms.get_positions()                   # positions of atoms (cartesian)
atoms.get_scaled_positions()            # positions of atoms (fractional)
# print(dir(atoms))

# etc, etc. see docs or help file for more
# or see a list of all methods/properties with:
# print(dir(atoms))

# # visualisation
# atoms.edit()

# # convert to pymatgen
# from pymatgen.io.ase import AseAtomsAdaptor
# atoms = AseAtomsAdaptor.get_atoms(structure)


# use function like this to loop through all cifs in a directory
import os
def read_cifs(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.cif'):
            atoms = ase.io.read(os.path.join(directory, filename))
            yield atoms, filename

# # use like:
# directory = '/path/to/cifs'
# for atoms, filename in read_cifs(directory):
#     pass