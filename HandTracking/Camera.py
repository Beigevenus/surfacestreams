from HandTracking.Point import Point
from HandTracking.image_wrap import four_point_transform as fpt

import cv2


class Camera:
    def __init__(self, drawarea, canvas, tmp_calibration_points, name='camera', camera=0):
        # TODO: Needs to be dynamically found
        self.capture = cv2.VideoCapture(camera)
        self.calibration_points = []
        self.sorted_calibration_points = tmp_calibration_points
        self.frame = self.update_frame()
        self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.name = name
        self.ptm = None
        self.warped_width = None
        self.warped_height = None
        self.drawarea = drawarea
        self.canvas = canvas

        cv2.namedWindow(self.name)
        cv2.setMouseCallback(self.name, self.mouse_click)

    def show_frame(self):
        self.draw_calibration_points()
        cv2.imshow(self.name, self.frame)

    def update_frame(self):
        success, self.frame = self.capture.read()
        self.frame = cv2.flip(self.frame, 1)
        if success:
            return self.frame
        return None

    def mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            if len(self.calibration_points) > 3:
                self.calibration_points.clear()
            elif len(self.calibration_points) == 3:
                self.calibration_points.append(Point(x, y))
                self.sorted_calibration_points = self.sort_calibration_points()
                self.drawarea.update_calibration_borders(self.sorted_calibration_points)
                self.update_image_ptm()
            else:
                self.calibration_points.append(Point(x, y))

    def draw_calibration_points(self):
        for point in self.calibration_points:
            cv2.circle(self.frame, (int(point.x), int(point.y)), int(int(10 / 2) * 2),
                       [255, 255, 0], cv2.FILLED)

    def update_image_ptm(self):
        if len(self.calibration_points) <= 3:
            None
        else:
            self.ptm, self.warped_width, self.warped_height = fpt(self.frame, self.sorted_calibration_points, self.canvas.width, self.canvas.height)

    def sort_calibration_points(self):
        left_top = left_bot = right_top = right_bot = None

        right_points = []
        left_top = self.calibration_points[0]
        left_bot = self.calibration_points[1]
        for point in self.calibration_points[2:]:
            temp = None
            if point.x < left_top.x:
                temp = left_top
                left_top = point
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
