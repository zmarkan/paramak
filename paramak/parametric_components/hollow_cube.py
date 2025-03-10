
import cadquery as cq
from paramak import Shape


class HollowCube(Shape):
    """A hollow cube with a constant thickness. Can be used to create a DAGMC
    Graveyard.

    Arguments:
        length (float): The length to use for the height, width, depth of the
            inner dimensions of the cube.
        thickness (float, optional): thickness of the vessel. Defaults to 10.0.
    """

    def __init__(
        self,
        length,
        thickness=10.,
        **kwargs
    ):
        self.length = length
        self.thickness = thickness
        super().__init__(
            **kwargs
        )

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    def create_solid(self):

        # creates a small box that surrounds the geometry
        inner_box = cq.Workplane("front").box(
            self.length,
            self.length,
            self.length
        )

        # creates a large box that surrounds the smaller box
        outer_box = cq.Workplane("front").box(
            self.length + self.thickness,
            self.length + self.thickness,
            self.length + self.thickness
        )

        # subtracts the two boxes to leave a hollow box
        new_shape = outer_box.cut(inner_box)

        self.solid = new_shape

        return new_shape
