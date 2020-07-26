from pymatgen.vis.structure_vtk import StructureVis, StructureInteractorStyle
from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor
import itertools
import numpy as np

import ase_tools

try:
    import vtk
except ImportError:
    vtk = None

"""
Wrapper for the class pymatgen.vis.structure_vtk.StructureVis
Keeps atoms unwrapped from the unit cell while using options in the drawer
"""
class WrappedStructureVis(StructureVis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style = WrappedStructureInteractorStyle(self)
        self.iren.SetInteractorStyle(style)
        self.ren.parent = self

    def redraw(self, reset_camera=False):
        """
        Redraw the render window.

        Args:
            reset_camera: Set to True to reset the camera to a
                pre-determined default for each structure.  Defaults to False.
        """
        self.ren.RemoveAllViewProps()
        self.picker = None
        self.add_picker_fixed()
        self.helptxt_mapper = vtk.vtkTextMapper()
        tprops = self.helptxt_mapper.GetTextProperty()
        tprops.SetFontSize(14)
        tprops.SetFontFamilyToTimes()
        tprops.SetColor(0, 0, 0)

        if self.structure is not None:
            self.set_structure(self.structure, reset_camera, to_unit_cell=self.wrapped)

        self.ren_win.Render()

    def display_help(self):
        """
        Display the help for various keyboard shortcuts.
        """
        helptxt = ["h : Toggle help",
                   "A/a, B/b or C/c : Increase/decrease cell by one a,"
                   " b or c unit vector", "# : Toggle showing of polyhedrons",
                   "-: Toggle showing of bonds", "r : Reset camera direction",
                   "w: Toggle wrapping into unit cell",
                   "[/]: Decrease or increase poly_radii_tol_factor "
                   "by 0.05. Value = " + str(self.poly_radii_tol_factor),
                   "Up/Down: Rotate view along Up direction by 90 "
                   "clockwise/anticlockwise",
                   "Left/right: Rotate view along camera direction by "
                   "90 clockwise/anticlockwise", "s: Save view to image.png",
                   "q: Quit"]
        self.helptxt_mapper.SetInput("\n".join(helptxt))
        self.helptxt_actor.SetPosition(10, 10)
        self.helptxt_actor.VisibilityOn()

    def set_structure(self, structure, reset_camera=False, to_unit_cell=False):
        """
        Add a structure to the visualizer.

        Args:
            structure: structure to visualize
            reset_camera: Set to True to reset the camera to a default
                determined based on the structure.
            to_unit_cell: Whether or not to fall back sites into the unit cell.
        """
        self.ren.RemoveAllViewProps()

        if not hasattr(self, 'wrapped'):
            self.wrapped = to_unit_cell
        if to_unit_cell:
            structure = structure.copy(sanitize=True)
        if not to_unit_cell:
            atoms = AseAtomsAdaptor.get_atoms(structure)
            atoms = ase_tools.unwrap(atoms)
            structure = AseAtomsAdaptor.get_structure(atoms)

        has_lattice = hasattr(structure, "lattice")

        if has_lattice:
            s = Structure.from_sites(structure, to_unit_cell)
            s.make_supercell(self.supercell, to_unit_cell)
        else:
            s = structure

        inc_coords = []
        for site in s:
            self.add_site(site)
            inc_coords.append(site.coords)

        count = 0
        labels = ["a", "b", "c"]
        colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

        if has_lattice:
            matrix = s.lattice.matrix

        if self.show_unit_cell and has_lattice:
            # matrix = s.lattice.matrix
            self.add_text([0, 0, 0], "o")
            for vec in matrix:
                self.add_line((0, 0, 0), vec, colors[count])
                self.add_text(vec, labels[count], colors[count])
                count += 1
            for (vec1, vec2) in itertools.permutations(matrix, 2):
                self.add_line(vec1, vec1 + vec2)
            for (vec1, vec2, vec3) in itertools.permutations(matrix, 3):
                self.add_line(vec1 + vec2, vec1 + vec2 + vec3)

        if self.show_bonds or self.show_polyhedron:
            elements = sorted(s.composition.elements, key=lambda a: a.X)
            anion = elements[-1]

            anion_radius = anion.average_ionic_radius
            for site in s:
                exclude = False
                max_radius = 0
                color = np.array([0, 0, 0])
                for sp, occu in site.species.items():
                    if sp.symbol in self.excluded_bonding_elements or sp == anion:
                        exclude = True
                        break
                    max_radius = max(max_radius, sp.average_ionic_radius)
                    color = color + occu * np.array(self.el_color_mapping.get(sp.symbol, [0, 0, 0]))

                if not exclude:
                    max_radius = (1 + self.poly_radii_tol_factor) * (max_radius + anion_radius)
                    nn = structure.get_neighbors(site, float(max_radius))
                    nn_sites = []
                    for neighbor in nn:
                        nn_sites.append(neighbor)
                    if self.show_bonds:
                        self.add_bonds(nn_sites, site)
                    if self.show_polyhedron:
                        color = [i / 255 for i in color]
                        self.add_polyhedron(nn_sites, site, color)

        if self.show_help:
            self.helptxt_actor = vtk.vtkActor2D()
            self.helptxt_actor.VisibilityOn()
            self.helptxt_actor.SetMapper(self.helptxt_mapper)
            self.ren.AddActor(self.helptxt_actor)
            self.display_help()

        camera = self.ren.GetActiveCamera()
        if reset_camera:
            if has_lattice:
                # Adjust the camera for best viewing
                lengths = s.lattice.abc
                pos = (matrix[1] + matrix[2]) * 0.5 + matrix[0] * max(lengths) / lengths[0] * 3.5
                camera.SetPosition(pos)
                camera.SetViewUp(matrix[2])
                camera.SetFocalPoint((matrix[0] + matrix[1] + matrix[2]) * 0.5)
            else:
                origin = s.center_of_mass
                max_site = max(
                    s, key=lambda site: site.distance_from_point(origin))
                camera.SetPosition(origin + 5 * (max_site.coords - origin))
                camera.SetFocalPoint(s.center_of_mass)

        self.structure = structure
        self.title = s.composition.formula

class WrappedStructureInteractorStyle(StructureInteractorStyle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, obj, event):
        parent = obj.GetCurrentRenderer().parent
        sym = parent.iren.GetKeySym()

        if sym in "ABCabc":
            if sym == "A":
                parent.supercell[0][0] += 1
            elif sym == "B":
                parent.supercell[1][1] += 1
            elif sym == "C":
                parent.supercell[2][2] += 1
            elif sym == "a":
                parent.supercell[0][0] = max(parent.supercell[0][0] - 1, 1)
            elif sym == "b":
                parent.supercell[1][1] = max(parent.supercell[1][1] - 1, 1)
            elif sym == "c":
                parent.supercell[2][2] = max(parent.supercell[2][2] - 1, 1)
            parent.redraw()
        elif sym == "w":
            parent.wrapped = not parent.wrapped
            parent.redraw()
        elif sym == "numbersign":
            parent.show_polyhedron = not parent.show_polyhedron
            parent.redraw()
        elif sym == "minus":
            parent.show_bonds = not parent.show_bonds
            parent.redraw()
        elif sym == "bracketleft":
            parent.poly_radii_tol_factor -= 0.05 \
                if parent.poly_radii_tol_factor > 0 else 0
            parent.redraw()
        elif sym == "bracketright":
            parent.poly_radii_tol_factor += 0.05
            parent.redraw()
        elif sym == "h":
            parent.show_help = not parent.show_help
            parent.redraw()
        elif sym == "r":
            parent.redraw(True)
        elif sym == "s":
            parent.write_image("image.png")
        elif sym == "Up":
            parent.rotate_view(1, 90)
        elif sym == "Down":
            parent.rotate_view(1, -90)
        elif sym == "Left":
            parent.rotate_view(0, -90)
        elif sym == "Right":
            parent.rotate_view(0, 90)

        self.OnKeyPress()
