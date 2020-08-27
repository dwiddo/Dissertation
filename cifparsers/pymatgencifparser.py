from pymatgen.io.cif import CifParser

# path to cif
cif_path = 'cifparsers/job_00001.cif'
parser = CifParser(cif_path)
structure = parser.get_structures()[0]      
# parser returns a list of all structures in one file, thus [0]

for s in parser.get_structures():
    print()



structure.frac_coords
structure.formula

structure.lattice
structure.lattice.lengths_and_angles

# see docs for more or use this to see all methods/properties:
# print(dir(structure))
# print(dir(structure.lattice))

# # visualisation
# from pymatgen.vis.structure_vtk import StructureVis
# vis = StructureVis(show_polyhedron=False)
# vis.set_structure(structure)
# vis.show()

# # convert to ase
# from pymatgen.io.ase import AseAtomsAdaptor
# structure = AseAtomsAdaptor.get_structure(atoms)
