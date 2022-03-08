from HandTracking.Config import Config
from HandTracking.Point import Point
from HandTracking.image_wrap import four_point_transform as fpt

import cv2


class Camera:
    def __init__(self, draw_area, canvas, calibration_points, name='camera', camera=0) -> None:
        # TODO: Needs to be dynamically found
        self.capture = cv2.VideoCapture(camera)
        self.calibration_points: list[Point] = calibration_points
        self.sorted_calibration_points: list[Point] = self.sort_calibration_points()
        self.frame = self.update_frame()
        self.height: int = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width: int = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.name: str = name
        self.ptm = None
        self.warped_width: int = None
        self.warped_height: int = None
        self.draw_area = draw_area
        self.canvas = canvas

        cv2.namedWindow(self.name)
        cv2.setMouseCallback(self.name, self.mouse_click)
        self.draw_area.update_calibration_borders(self.sorted_calibration_points)
        self.update_image_ptm()

    def show_frame(self) -> None:
        """
        Shows the current camera frame in its window.
        """
        self.draw_calibration_points()
        cv2.imshow(self.name, self.frame)

    def update_frame(self):
        success, self.frame = self.capture.read()
        self.frame = cv2.flip(self.frame, 1)
        if success:
            return self.frame
        return None

    def mouse_click(self, event, x, y, flags, param) -> None:
        if event == cv2.EVENT_LBUTTONUP:
            if len(self.calibration_points) > 3:
                self.calibration_points.clear()
            elif len(self.calibration_points) == 3:
                self.calibration_points.append(Point(x, y))
                self.sorted_calibration_points = self.sort_calibration_points()
                self.draw_area.update_calibration_borders(self.sorted_calibration_points)
                self.update_image_ptm()
                Config.save_calibration_points(self.calibration_points)
            else:
                self.calibration_points.append(Point(x, y))

    def draw_calibration_points(self) -> None:
        for point in self.calibration_points:
            cv2.circle(self.frame, (int(point.x), int(point.y)), int(int(10 / 2) * 2),
                       [255, 255, 0], cv2.FILLED)

    @staticmethod
    def return_camera_indexes():
        # checks the first 20 indexes.
        index = 0
        arr = []
        i = 20
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr

    def update_image_ptm(self):
        if len(self.calibration_points) <= 3:
            None
        else:
            self.ptm, self.warped_width, self.warped_height = fpt(self.frame, self.sorted_calibration_points, self.canvas.width, self.canvas.height)

    def sort_calibration_points(self) -> list[Point]:
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
