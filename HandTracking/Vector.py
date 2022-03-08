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
        """
        Calculates the dot product of two vectors, namely, itself and other.

        :param other: The other vector to calculate the dot product with
        :return: The dot product of self and other
        """
        return (self.x * other.x) + (self.y * other.y)

    # TODO: Vulnerable to DivisionByZeroError, fix this
    def angle_between(self, other: 'Vector') -> float:
        """
        Calculates and returns the cosine of the angle between two vectors, namely, itself and other.

        :param other: The vector to calculate the angle to
        :return: The angle between self and other
        """
        return (self.dot(other)) / (self.length * other.length)
