from math import sqrt, pow

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def distance_to(self, other):
        calculation = pow(self.x - other.x, 2) + pow(self.y - other.y, 2)
        return sqrt(calculation)

    def get_position_on_canvas(self, area_width, area_height, canvas_width, canvas_height):
        """
        Get the position of the point in the actual canvas
        """
        x = canvas_width * (canvas_width * (self.x / area_width) / canvas_width)
        y = canvas_height * (canvas_height * (self.y / area_height) / canvas_height)
        return Point(x, y)
