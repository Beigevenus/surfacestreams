import math


class Vector:
    def __init__(self, start_p, end_p) -> None:
        self.x = end_p.x - start_p.x
        self.y = end_p.y - start_p.y
        self.length = start_p.distance_to(end_p)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y)
    
    def angle_between(self, other):
        return math.acos((self.dot(other)) / (self.length * other.length))