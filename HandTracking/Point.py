from math import sqrt, pow

class Point:
    def __init__(self, *args) -> None:
        #TODO: refactor
        if len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        elif len(args) == 1:
            self.x = args[0].x
            self.y = args[0].y


    def distance_to(self, other):
        calculation = pow(self.x - other.x, 2) + pow(self.y - other.y, 2)
        return sqrt(calculation)

    def offset_to(self, other, precision=2):
        point = self.midpoint_to(other)

        for i in range(0, precision):
            point = self.midpoint_to(point)

        return point

    def midpoint_to(self, other):
        return Point((self.x + other.x)/2, (self.y + other.y)/2)

    def get_position_on_canvas(self, area_width, area_height, canvas_width, canvas_height):
        """
        Get the position of the point in the actual canvas
        """
        x = canvas_width * (canvas_width * (self.x / area_width) / canvas_width)
        y = canvas_height * (canvas_height * (self.y / area_height) / canvas_height)
        return Point(x, y)
