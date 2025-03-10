
import unittest

import paramak
import pytest


class TestBlanketConstantThicknessArcH(unittest.TestCase):

    def setUp(self):
        self.test_shape = paramak.BlanketConstantThicknessArcH(
            inner_lower_point=(300, -200),
            inner_mid_point=(500, 0),
            inner_upper_point=(300, 200),
            thickness=20,
        )

    def test_default_parameters(self):
        """Checks that the default parameters of a BlanketConstantThicknessArcH are correct."""

        assert self.test_shape.rotation_angle == 360

    def test_points_calculation(self):
        """Checks that the points used to construct the BlanketConstantThicknessArcH component
        are calculated correctly from the parameters given."""

        assert self.test_shape.points == [
            (300, 200, 'circle'),
            (500, 0, 'circle'),
            (300, -200, 'straight'),
            (320, -200, 'circle'),
            (520, 0, 'circle'),
            (320, 200, 'straight')
        ]

    def test_processed_points_calculation(self):
        """Checks that the processed_points used to construct the
        BlanketConstantThicknessArcH component are calculated correctly from
        the parameters given."""

        assert self.test_shape.processed_points == [
            (300, 200, 'circle'),
            (500, 0, 'circle'),
            (300, -200, 'straight'),
            (320, -200, 'circle'),
            (520, 0, 'circle'),
            (320, 200, 'straight'),
            (300, 200, 'circle')
        ]

    def test_component_creation(self):
        """Creates a blanket using the BlanketConstantThicknessArcH parametric
        component and checks that a cadquery solid is created."""

        assert self.test_shape.solid is not None
        assert self.test_shape.volume() > 1000

    def test_relative_shape_volume(self):
        """Creates two blankets using the BlanketConstantThicknessArcH parametric component
        and checks that their relative volumes are correct."""

        test_volume = self.test_shape.volume()
        self.test_shape.rotation_angle = 180
        assert test_volume == pytest.approx(self.test_shape.volume() * 2)

    def test_shape_face_areas(self):
        """Creates a blanket using the BlanketConstantThicknessArcH parametric component and
        checks that the face areas are expected."""

        assert len(self.test_shape.areas) == 4
        assert len(set([round(i) for i in self.test_shape.areas])) == 3

        self.test_shape.rotation_angle = 180
        assert len(self.test_shape.areas) == 6
        assert len(set([round(i) for i in self.test_shape.areas])) == 4
