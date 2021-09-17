from typing import List, Optional

import paramak


class CylinderReactor(paramak.Reactor):
    """Creates the 3D geometry for the cylinder reactor model based on
    parameters.

    Args:
        inner_blanket_radius: The radial distance between the center of the
            reactor on the start of the blanket (cm).
        blanket_thickness: The radial thickness of the blanket (cm).
        blanket_height: The height (z axis direction) of the blanket (cm).
        lower_blanket_thickness: The thickness (z axis direction) of the
            lower blanket pool (cm).
        blanket_vv_gap: The radial distance between the outer edge of the
            blanket and the inner edge of the vaccum vessel (cm).
        upper_vv_thickness: The thickness (z axis direction) of the
            the upper section of vaccum vessel (cm).
        vv_thickness: The radial thickness of the vaccum vessel (cm)
        lower_vv_thickness: The thickness (z axis direction) of the
            the lower section of vaccum vessel (cm).
        rotation_angle: The angle of the sector simulated. Set to 360 for
            simulations and less when creating models for visualization.
    Returns:
        paramak.Reactor object
    """

    def __init__(
        self,
        inner_blanket_radius: Optional[float] = 100,
        blanket_thickness: Optional[float] = 60,
        blanket_height: Optional[float] = 500,
        lower_blanket_thickness: Optional[float] = 50,
        upper_blanket_thickness: Optional[float] = 40,
        blanket_vv_gap: Optional[float] = 20,
        upper_vv_thickness: Optional[float] = 10,
        vv_thickness: Optional[float] = 10,
        lower_vv_thickness: Optional[float] = 10,
        rotation_angle: Optional[float] = 360,
    ):

        super().__init__([])

        self.rotation_angle = rotation_angle
        self.inner_blanket_radius = inner_blanket_radius
        self.blanket_thickness = blanket_thickness
        self.blanket_height = blanket_height
        self.lower_blanket_thickness = lower_blanket_thickness
        self.upper_blanket_thickness = upper_blanket_thickness
        self.blanket_vv_gap = blanket_vv_gap
        self.upper_vv_thickness = upper_vv_thickness
        self.vv_thickness = vv_thickness
        self.lower_vv_thickness = lower_vv_thickness

        # makes a list of the input arguments, use in reactor.input_variables
        self.input_variable_names = paramak.Reactor().input_variable_names + [
            elem for elem in list(locals().keys()) if elem not in ["shapes_and_components", "self", "__class__"]
        ]

    def create_solids(self):
        """Creates a list of paramak.Shape for components and saves it in
        self.shapes_and_components
        """
        inner_wall = (
            self.inner_blanket_radius +
            self.blanket_thickness +
            self.blanket_vv_gap)
        lower_vv = paramak.RotateStraightShape(
            points=[
                (inner_wall,
                 (-self.blanket_height / 2.0) - self.lower_blanket_thickness,
                 ),
                (inner_wall,
                 (-self.blanket_height / 2.0) - (
                     self.lower_blanket_thickness + self.lower_vv_thickness),
                 ),
                (0,
                 (-self.blanket_height / 2.0) - (
                     self.lower_blanket_thickness + self.lower_vv_thickness),
                 ),
                (0,
                 (-self.blanket_height / 2.0) - self.lower_blanket_thickness),
            ],
            rotation_angle=self.rotation_angle,
            stp_filename="lower_vv.stp",
            material_tag="vv_mat",
            color=(
                0.5,
                0.5,
                0.5),
            name="lower vacuum vessel",
        )

        lower_blanket = paramak.RotateStraightShape(
            points=[
                (inner_wall, -self.blanket_height / 2.0),
                (
                    inner_wall,
                    (-self.blanket_height / 2.0) - self.lower_blanket_thickness,
                ),
                (0, (-self.blanket_height / 2.0) - self.lower_blanket_thickness),
                (0, -self.blanket_height / 2.0),
            ],
            rotation_angle=self.rotation_angle,
            stp_filename="lower_blanket.stp",
            material_tag="blanket_mat",
            color=(0.0, 1.0, 0.498),
            name="lower blanket",
        )

        blanket = paramak.CenterColumnShieldCylinder(
            height=self.blanket_height,
            inner_radius=self.inner_blanket_radius,
            outer_radius=self.blanket_thickness + self.inner_blanket_radius,
            rotation_angle=self.rotation_angle,
            stp_filename="blanket.stp",
            cut=lower_blanket,
            material_tag="blanket_mat",
            color=(0.0, 1.0, 0.498),
            name="blanket",
        )

        upper_blanket = paramak.RotateStraightShape(
            points=[
                (inner_wall, (self.blanket_height / 2.0) + self.upper_vv_thickness),
                (
                    inner_wall,
                    (self.blanket_height / 2.0)
                    + self.upper_vv_thickness
                    + self.upper_blanket_thickness,
                ),
                (
                    0,
                    (self.blanket_height / 2.0)
                    + self.upper_vv_thickness
                    + self.upper_blanket_thickness,
                ),
                (0, (self.blanket_height / 2.0) + self.upper_vv_thickness),
            ],
            rotation_angle=self.rotation_angle,
            stp_filename="upper_blanket.stp",
            material_tag="blanket_mat",
            color=(0.0, 1.0, 0.498),
            name="upper blanket",
        )

        upper_vv = paramak.RotateStraightShape(
            points=[
                (inner_wall, self.blanket_height / 2.0),
                (inner_wall, (self.blanket_height / 2.0) + self.upper_vv_thickness),
                (0, (self.blanket_height / 2.0) + self.upper_vv_thickness),
                (0, self.blanket_height / 2.0),
            ],
            rotation_angle=self.rotation_angle,
            stp_filename="upper_vv.stp",
            material_tag="vv_mat",
            color=(0.5, 0.5, 0.5),
            name="upper vacuum vessel",
        )

        vac_ves = paramak.RotateStraightShape(
            points=[
                (
                    inner_wall + self.vv_thickness,
                    (self.blanket_height / 2.0)
                    + self.upper_vv_thickness
                    + self.upper_blanket_thickness,
                ),
                (
                    inner_wall,
                    (self.blanket_height / 2.0)
                    + self.upper_vv_thickness
                    + self.upper_blanket_thickness,
                ),
                (
                    inner_wall,
                    -(self.blanket_height / 2.0)
                    - self.lower_blanket_thickness
                    - self.lower_vv_thickness,
                ),
                (
                    inner_wall + self.vv_thickness,
                    -(self.blanket_height / 2.0)
                    - self.lower_blanket_thickness
                    - self.lower_vv_thickness,
                ),
            ],
            rotation_angle=self.rotation_angle,
            stp_filename="vv.stp",
            material_tag="vv_mat",
            color=(0.5, 0.5, 0.5),
            name="vacuum vessel",
        )

        self.shapes_and_components = [
            blanket,
            vac_ves,
            upper_blanket,
            lower_blanket,
            lower_vv,
            upper_vv,
        ]
