import numpy as np
from numpy import polyfit, ndarray
from HandTracking.Point import Point


class DrawArea:
    def __init__(self, calibration_points: list[Point]) -> None:
        self.left_border: list[float] = self.get_line_attributes(calibration_points[0], calibration_points[2])
        self.right_border: list[float] = self.get_line_attributes(calibration_points[1], calibration_points[3])
        self.top_border: list[float] = self.get_line_attributes(calibration_points[0], calibration_points[1])
        self.bottom_border: list[float] = self.get_line_attributes(calibration_points[2], calibration_points[3])

    def update_calibration_borders(self, calibration_points: list[Point]) -> None:
        # TODO: Write docstring for method
        self.left_border = self.get_line_attributes(calibration_points[0], calibration_points[2])
        self.right_border = self.get_line_attributes(calibration_points[1], calibration_points[3])
        self.top_border = self.get_line_attributes(calibration_points[0], calibration_points[1])
        self.bottom_border = self.get_line_attributes(calibration_points[2], calibration_points[3])

    def get_position_on_canvas(self, point: Point, ptm: ndarray) -> Point:
        # TODO: Write docstring for method
        # Does matrix multiplication on the perspective transform matrix and the original
        # position of the finger on the camera
        corrected_coordinates = np.matmul(ptm, [
            point.x,
            point.y, 1])

        corrected_point = Point(corrected_coordinates[0], corrected_coordinates[1])

        # x = canvas_width * (corrected_point.x / area_width)
        # y = canvas_height * (corrected_point.y / area_height)
        return corrected_point  # Point(x, y)

    def is_position_in_calibration_area(self, point: Point) -> bool:
        """
        Determines whether the given point is within the zone created by the calibration points.

        :param point: The point to check
        :return: True or False depending on whether it is inside or outside the calibration area
        """
        # y = ax+b
        top_border_point: Point = Point(point.x, self.top_border[0] * point.x + self.top_border[1])
        if top_border_point.y >= point.y:
            return False
        bottom_border_point: Point = Point(point.x, self.bottom_border[0] * point.x + self.bottom_border[1])
        if bottom_border_point.y <= point.y:
            return False
        # x = (y-b) / a
        if self.left_border[0] is None:
            left_border_point: Point = Point(self.left_border[1], point.y)
        else:
            left_border_point = Point((point.y - self.left_border[1]) / self.left_border[0], point.y)
        if left_border_point.x > point.x:
            return False

        if self.right_border[0] is None:
            right_border_point: Point = Point(self.right_border[1], point.y)
        else:
            right_border_point = Point((point.y - self.right_border[1]) / self.right_border[0], point.y)
        if right_border_point.x < point.x:
            return False

        return True

    def get_line_attributes(self, point1: Point, point2: Point) -> list[float]:
        # TODO: Write docstring for method
        if point2.x == point1.x:
            # When the line is vertical the gradient is set to None and the b value should be used for further
            # calculations
            return [None, point1.x]
        a: float = (point2.y - point1.y) / (point2.x - point1.x)
        b: float = point1.y - (a * point1.x)

        return [a, b]

