import math

from HandTracking.Point import Point


class Vector:
    def __init__(self, start_p: Point, end_p: Point) -> None:
        self.x: float = end_p.x - start_p.x
        self.y: float = end_p.y - start_p.y
        self.length: float = start_p.distance_to(end_p)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def dot(self, other) -> float:
        return (self.x * other.x) + (self.y * other.y)
    
    def angle_between(self, other: 'Vector') -> float:
        return (self.dot(other)) / (self.length * other.length)
