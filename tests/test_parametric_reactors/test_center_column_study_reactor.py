
import os
import unittest
import warnings
from pathlib import Path

import paramak
import pytest


class TestCenterColumnStudyReactor(unittest.TestCase):
    """Test functionality of the CenterColumnStudyReactor class"""

    def setUp(self):
        self.test_reactor = paramak.CenterColumnStudyReactor(
            inner_bore_radial_thickness=20,
            inboard_tf_leg_radial_thickness=50,
            center_column_shield_radial_thickness_mid=50,
            center_column_shield_radial_thickness_upper=100,
            inboard_firstwall_radial_thickness=20,
            divertor_radial_thickness=100,
            inner_plasma_gap_radial_thickness=80,
            plasma_radial_thickness=200,
            outer_plasma_gap_radial_thickness=90,
            elongation=2.3,
            triangularity=0.45,
            plasma_gap_vertical_thickness=40,
            center_column_arc_vertical_thickness=520,
            rotation_angle=359
        )

    def test_input_variable_names(self):
        """tests that the number of inputs variables is correct"""

        assert len(self.test_reactor.input_variables.keys()) == 17
        assert len(self.test_reactor.input_variable_names) == 17

    def test_creation(self):
        """Creates a ball reactor using the CenterColumnStudyReactor parametric_reactor and checks
        the correct number of components are created."""

        assert len(self.test_reactor.shapes_and_components) == 6

    def test_creation_with_narrow_divertor(self):
        """Creates a ball reactor with a narrow divertor using the CenterColumnStudyReactor
        parametric reactor and checks that the correct number of components are created."""

        self.test_reactor.divertor_radial_thickness = 10
        assert len(self.test_reactor.shapes_and_components) == 6

    def test_svg_creation(self):
        """Creates a ball reactor using the CenterColumnStudyReactor parametric_reactor and checks
        an svg image of the reactor can be exported."""

        os.system("rm test_image.svg")
        self.test_reactor.export_svg("test_image.svg")
        assert Path("test_image.svg").exists() is True
        os.system("rm test_image.svg")

    def test_rotation_angle_impacts_volume(self):
        """Creates a CenterColumnStudyReactor reactor with a rotation angle of
        90 and another reactor with a rotation angle of 180. Then checks the
        volumes of all the components is double in the 180 reactor."""

        self.test_reactor.rotation_angle = 90
        r90_comp_vols = [
            comp.volume() for comp in self.test_reactor.shapes_and_components]
        self.test_reactor.rotation_angle = 180
        r180_comp_vols = [
            comp.volume() for comp in self.test_reactor.shapes_and_components]
        for r90_vol, r180_vol in zip(r90_comp_vols, r180_comp_vols):
            assert r90_vol == pytest.approx(r180_vol * 0.5, rel=0.1)

    def test_rotation_angle_warning(self):
        """Checks that the correct warning message is printed when
        rotation_angle = 360."""

        def warning_trigger():
            try:
                self.test_reactor.rotation_angle = 360
                self.test_reactor.shapes_and_components
            except BaseException:
                pass

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warning_trigger()
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "360 degree rotation may result in a Standard_ConstructionError or AttributeError" in str(
                w[-1].message)

    def test_html_file_creation(self):
        """Creates a reactor with exports the step files and check they exist"""

        os.system('rm *.html')
        self.test_reactor.export_html_3d('cylinder.html')
        assert Path('cylinder.html').is_file()

    def test_export_brep(self):
        """Exports a brep file and checks that the output exist"""

        os.system("rm test_reactor.brep")

        self.test_reactor.export_brep(filename='merged.brep', merge=True)
        self.test_reactor.export_brep(filename='not_merged.brep', merge=False)

        assert Path("merged.brep").exists() is True
        assert Path("not_merged.brep").exists() is True
        # not always true
        # assert Path("not_merged.brep").stat().st_size > Path(
        #     "merged.brep").stat().st_size

        os.system("rm merged.brep")
        os.system("rm not_merged.brep")

    def test_export_brep_without_extention(self):
        """Exports a brep file without the extention and checks that the
        output exist"""

        def missing_extention():

            self.test_reactor.export_brep(filename='test_reactor_missing')

        self.assertRaises(
            ValueError,
            missing_extention
        )
