from math import sqrt, pow

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def distance(self, other):
        calculation = pow(self.x - other.x, 2) + pow(self.y - other.y, 2)
        return sqrt(calculation)