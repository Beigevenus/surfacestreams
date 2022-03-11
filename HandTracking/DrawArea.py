import numpy as np
from numpy import polyfit
from HandTracking.Camera import Camera
from HandTracking.Canvas import Canvas
from HandTracking.Point import Point


class DrawArea:
    def __init__(self, calibration_points):
        self.left_border = self.get_line_attributes(calibration_points[0], calibration_points[2])
        self.right_border = self.get_line_attributes(calibration_points[1], calibration_points[3])
        self.top_border = self.get_line_attributes(calibration_points[0], calibration_points[1])
        self.bottom_border = self.get_line_attributes(calibration_points[2], calibration_points[3])

    def update_calibration_borders(self, calibration_points):
        self.left_border = self.get_line_attributes(calibration_points[0], calibration_points[2])
        self.right_border = self.get_line_attributes(calibration_points[1], calibration_points[3])
        self.top_border = self.get_line_attributes(calibration_points[0], calibration_points[1])
        self.bottom_border = self.get_line_attributes(calibration_points[2], calibration_points[3])

    def get_position_on_canvas(self, point, canvas: Canvas, camera: Camera):
        """
        Get the position of the point in the actual canvas
        """
        # Does matrix multipication on the perspective transform matrix and the original
        # position of the finger on the camera
        corrected_coordinates = np.matmul(camera.ptm, [
            point.x,
            point.y, 1])

        ########################### Midlertidig løsning ############################
        normalized_coordinates = Point(round(corrected_coordinates[0]) / camera.warped_width, round(corrected_coordinates[1]) / camera.warped_height)

        corrected_point = Point(round(normalized_coordinates.x * canvas.width), round(normalized_coordinates.y * canvas.height))

        # x = canvas_width * (corrected_point.x / area_width)
        # y = canvas_height * (corrected_point.y / area_height)
        return corrected_point # Point(x, y)

    def is_position_in_calibration_area(self, point):
        # y = ax+b
        top_border_point = Point(point.x, self.top_border[0] * point.x + self.top_border[1])
        if top_border_point.y >= point.y:
            return False
        bottom_border_point = Point(point.x, self.bottom_border[0] * point.x + self.bottom_border[1])
        if bottom_border_point.y <= point.y:
            return False
        # x = (y-b) / a
        if self.left_border[0] is None:
            left_border_point = Point(self.left_border[1], point.y)
        else:
            left_border_point = Point((point.y - self.left_border[1]) / self.left_border[0], point.y)
        if left_border_point.x > point.x:
            return False

        if self.right_border[0] is None:
            right_border_point = Point(self.right_border[1], point.y)
        else:
            right_border_point = Point((point.y - self.right_border[1]) / self.right_border[0], point.y)
        if right_border_point.x < point.x:
            return False

        return True

    def get_line_attributes(self, point1, point2):
        if point2.x == point1.x:
            # When the line is vertical the gradient is set to None and the b value should be used for further calculations
            return [None, point1.x]
        a = (point2.y-point1.y) / (point2.x-point1.x)
        b = point1.y - (a*point1.x)

        return[a, b]

