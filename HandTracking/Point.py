from math import sqrt, pow
from numpy import polyfit


class Point:
    def __init__(self, x, y) -> None:
        self.x: float = x
        self.y: float = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    @classmethod
    def from_landmark(cls, landmark) -> 'Point':
        """
        Overload of the constructor, which gives a Point object from a landmark.

        :param landmark: The landmark to extract coordinates from
        :return: A Point object containing the x and y of the landmark
        """
        x: float = landmark.x
        y: float = landmark.y

        return cls(x, y)

    @classmethod
    def from_dict(cls, dictionary) -> 'Point':
        x: float = dictionary["x"]
        y: float = dictionary["y"]

        return cls(x, y)

    def distance_to(self, other) -> float:
        """
        Calculates the distance between itself an another Point object.

        :param other: The other Point to calculate the distance to
        :return: The distance between self and other
        """
        calculation: float = (self.x - other.x) ** 2 + (self.y - other.y) ** 2
        return sqrt(calculation)

    def offset_to(self, other, precision=2):
        point = self.midpoint_to(other)

        for i in range(0, precision):
            point = self.midpoint_to(point)

        return point

    def midpoint_to(self, other):
        return Point((self.x + other.x)/2, (self.y + other.y)/2)

    def get_position_on_canvas(self, area_width, area_height, canvas_width, canvas_height) -> 'Point':
        """
        Gets the position of the Point in the actual canvas given its current position.

        :param area_width: The width of the area the current Point exists within
        :param area_height: The height of the area the current Point exists within
        :param canvas_width: The width of the canvas
        :param canvas_height: The height of the canvas
        :return: A new Point object with coordinates corresponding to the position on the canvas
        """
        x: float = canvas_width * (canvas_width * (self.x / area_width) / canvas_width)
        y: float = canvas_height * (canvas_height * (self.y / area_height) / canvas_height)
        return Point(x, y)

    def as_array(self):
        return [self.x, self.y]
