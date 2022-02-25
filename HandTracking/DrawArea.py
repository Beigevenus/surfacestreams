import numpy
from numpy import polyfit
from HandTracking.Point import Point


class DrawArea:
    def __init__(self, calibration_points):
        self.sorted_calibration_points = self.sort_calibration_points(calibration_points)

        try:
            self.left_border = polyfit(self.sorted_calibration_points[0].as_array(), self.sorted_calibration_points[2].as_array(), 1)
        except numpy.linalg.LinAlgError:
            self.left_border = 'Vertical'
        try:
            self.right_border = polyfit(self.sorted_calibration_points[1].as_array(), self.sorted_calibration_points[3].as_array(), 1)
        except numpy.linalg.LinAlgError:
            self.right_border = 'Vertical'
        self.top_border = polyfit(self.sorted_calibration_points[0].as_array(), self.sorted_calibration_points[1].as_array(), 1)
        self.bottom_border = polyfit(self.sorted_calibration_points[2].as_array(), self.sorted_calibration_points[3].as_array(), 1)

    def set_calibration_points(self, calibration_points):
        self.sorted_calibration_points = self.sort_calibration_points(calibration_points)

        try:
            self.left_border = polyfit(self.sorted_calibration_points[0].as_array(),
                                       self.sorted_calibration_points[2].as_array(), 1)
        except numpy.linalg.LinAlgError:
            self.left_border = 'Vertical'
        try:
            self.right_border = polyfit(self.sorted_calibration_points[1].as_array(),
                                        self.sorted_calibration_points[3].as_array(), 1)
        except numpy.linalg.LinAlgError:
            self.right_border = 'Vertical'
        self.top_border = polyfit(self.sorted_calibration_points[0].as_array(),
                                  self.sorted_calibration_points[1].as_array(), 1)
        self.bottom_border = polyfit(self.sorted_calibration_points[2].as_array(),
                                     self.sorted_calibration_points[3].as_array(), 1)

    def get_position_on_canvas(self, canvas_width, canvas_height, point):
        """
        Get the position of the point in the actual canvas
        """
        # y = ax+b
        top_border_point = Point(point.x, self.top_border[0] * point.x + self.top_border[1])
        bottom_border_point = Point(point.x, self.bottom_border[0] * point.x + self.bottom_border[1])
        # x = (y-b) / a
        left_border_point = Point((point.y - self.left_border[1]) / self.left_border[0], point.y)
        right_border_point = Point((point.y - self.right_border[1]) / self.right_border[0], point.y)

        vertical_distance = bottom_border_point.y - top_border_point.y
        horisontal_distance = right_border_point.x - left_border_point.x

        vertical_relation = (bottom_border_point.y - point.y) / vertical_distance
        horisontal_relation = (right_border_point.x - point.x) / horisontal_distance

        if vertical_relation <= 1 and horisontal_relation <= 1:
            x = canvas_width * horisontal_relation
            y = canvas_height * vertical_relation
            return Point(x, y)
        else:
            return None

    def sort_calibration_points(self, calibration_points):
        left_top = left_bot = right_top = right_bot = None

        right_points = []
        left_top = calibration_points[0]
        left_bot = calibration_points[1]
        for point in calibration_points[2:]:
            temp = None
            if point.x < left_top.x:
                temp = left_top
                left_top = point.x
            else:
                temp = point
            if temp.x < left_bot.x:
                right_points.append(left_bot)
                left_bot = temp
            else:
                right_points.append(temp)

        right_top = right_points[0]
        right_bot = right_points[1]

        if left_top.y > left_bot.y:
            temp = left_top
            left_top = left_bot
            left_bot = temp

        if right_top.y > right_bot.y:
            temp = right_top
            right_top = right_bot
            right_bot = temp

        return [left_top, right_top, left_bot, right_bot]
