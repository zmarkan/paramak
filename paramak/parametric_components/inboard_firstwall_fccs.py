
from collections.abc import Iterable
from typing import List, Optional, Tuple

from paramak import (CenterColumnShieldCircular, CenterColumnShieldCylinder,
                     CenterColumnShieldFlatTopCircular,
                     CenterColumnShieldFlatTopHyperbola,
                     CenterColumnShieldHyperbola,
                     CenterColumnShieldPlasmaHyperbola, RotateMixedShape)
import paramak


class InboardFirstwallFCCS(RotateMixedShape):
    """An inboard firstwall component that builds a constant thickness layer
    from the central column shield. The center column shields can be of type:
    CenterColumnShieldCylinder, CenterColumnShieldHyperbola,
    CenterColumnShieldFlatTopHyperbola, CenterColumnShieldCircular,
    CenterColumnShieldPlasmaHyperbola or CenterColumnShieldFlatTopCircular

    Args:
        central_column_shield: The central column shield object to build from
        thickness: the radial thickness of the firstwall (cm)
    """

    def __init__(
        self,
        central_column_shield: paramak.Shape,
        thickness: float,
        color: Optional[Tuple[float, float, float, Optional[float]]] = (0.5, 0.5, 0.5),
        **kwargs
    ):

        super().__init__(
            color=color,
            **kwargs
        )

        self.central_column_shield = central_column_shield
        self.thickness = thickness

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value

    @property
    def central_column_shield(self):
        return self._central_column_shield

    @central_column_shield.setter
    def central_column_shield(self, value):
        self._central_column_shield = value

    def find_points(self):

        # check that is an acceptable class
        acceptable_classes = (
            CenterColumnShieldCylinder,
            CenterColumnShieldHyperbola,
            CenterColumnShieldFlatTopHyperbola,
            CenterColumnShieldPlasmaHyperbola,
            CenterColumnShieldCircular,
            CenterColumnShieldFlatTopCircular
        )
        if not isinstance(self.central_column_shield, acceptable_classes):
            raise ValueError(
                "InboardFirstwallFCCS.central_column_shield must be an \
                instance of CenterColumnShieldCylinder, \
                CenterColumnShieldHyperbola, \
                CenterColumnShieldFlatTopHyperbola, \
                CenterColumnShieldPlasmaHyperbola, \
                CenterColumnShieldCircular, CenterColumnShieldFlatTopCircular")

        inner_radius = self.central_column_shield.inner_radius
        height = self.central_column_shield.height

        if isinstance(self.central_column_shield, CenterColumnShieldCylinder):
            firstwall = CenterColumnShieldCylinder(
                height=height,
                inner_radius=inner_radius,
                outer_radius=self.central_column_shield.outer_radius +
                self.thickness
            )

        elif isinstance(self.central_column_shield,
                        CenterColumnShieldHyperbola):
            firstwall = CenterColumnShieldHyperbola(
                height=height,
                inner_radius=inner_radius,
                mid_radius=self.central_column_shield.mid_radius +
                self.thickness,
                outer_radius=self.central_column_shield.outer_radius +
                self.thickness,
            )

        elif isinstance(self.central_column_shield,
                        CenterColumnShieldFlatTopHyperbola):
            firstwall = CenterColumnShieldFlatTopHyperbola(
                height=height,
                arc_height=self.central_column_shield.arc_height,
                inner_radius=inner_radius,
                mid_radius=self.central_column_shield.mid_radius +
                self.thickness,
                outer_radius=self.central_column_shield.outer_radius +
                self.thickness,
            )

        elif isinstance(self.central_column_shield,
                        CenterColumnShieldPlasmaHyperbola):
            firstwall = CenterColumnShieldPlasmaHyperbola(
                height=height,
                inner_radius=inner_radius,
                mid_offset=self.central_column_shield.mid_offset -
                self.thickness,
                edge_offset=self.central_column_shield.edge_offset -
                self.thickness,
            )

        elif isinstance(self.central_column_shield,
                        CenterColumnShieldCircular):
            firstwall = CenterColumnShieldCircular(
                height=height,
                inner_radius=inner_radius,
                mid_radius=self.central_column_shield.mid_radius +
                self.thickness,
                outer_radius=self.central_column_shield.outer_radius +
                self.thickness,
            )

        elif isinstance(self.central_column_shield,
                        CenterColumnShieldFlatTopCircular):
            firstwall = CenterColumnShieldFlatTopCircular(
                height=height,
                arc_height=self.central_column_shield.arc_height,
                inner_radius=inner_radius,
                mid_radius=self.central_column_shield.mid_radius +
                self.thickness,
                outer_radius=self.central_column_shield.outer_radius +
                self.thickness,
            )

        firstwall.rotation_angle = self.rotation_angle
        self.connection_type = firstwall.connection_type
        self.points = firstwall.points

        # add to cut attribute
        if self.cut is None:
            self.cut = self.central_column_shield
        elif isinstance(self.cut, Iterable):
            self.cut = [*self.cut, self.central_column_shield]
        else:
            self.cut = [*[self.cut], self.central_column_shield]
