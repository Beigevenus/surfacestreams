from math import sqrt, pow
from numpy import polyfit


class Point:
    def __init__(self, *args) -> None:
        #TODO: refactor
        if len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        elif len(args) == 1:
            self.x = args[0].x
            self.y = args[0].y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def distance_to(self, other):
        calculation = pow(self.x - other.x, 2) + pow(self.y - other.y, 2)
        return sqrt(calculation)

    def as_array(self):
        return [self.x, self.y]
