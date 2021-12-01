
from typing import Optional, Tuple

from paramak import Shape


class RotateMixedShape(Shape):
    """Rotates a 3d CadQuery solid from points connected with a mixture of
    straight lines and splines.

    Args:
        rotation_angle: The rotation_angle to use when revolving the solid
            (degrees). Defaults to 360.0.
    """

    def __init__(
        self,
        rotation_angle: Optional[float] = 360.,
        color: Optional[Tuple[float, float, float, Optional[float]]] = (0.121, 0.47, 0.705),
        name: str = 'rotatemixedshape',
        **kwargs
    ):

        super().__init__(
            color=color,
            name=name,
            **kwargs
        )
        self.rotation_angle = rotation_angle
        self.color = color
        self.name = name

    @property
    def rotation_angle(self):
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, value):
        self._rotation_angle = value

    def create_solid(self):
        """Creates a rotated 3d solid using points with straight and spline
        edges.

           Returns:
              A CadQuery solid: A 3D solid volume
        """

        solid = super().create_solid()

        wire = solid.close()

        self.wire = wire

        solid = wire.revolve(self.rotation_angle)

        solid = self.rotate_solid(solid)
        solid = self.perform_boolean_operations(solid)
        self.solid = solid
        return solid
