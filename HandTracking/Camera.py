from typing import List, Optional

from cv2 import VideoCapture
from numpy import ndarray

from HandTracking.Canvas import Canvas
from HandTracking.Config import Config
from HandTracking.DrawArea import DrawArea
from HandTracking.Point import Point
from HandTracking.image_wrap import four_point_transform as fpt

import cv2


class Camera:
    def __init__(self, draw_area: DrawArea, canvas: Canvas, calibration_points: list[Point], name: str = 'camera',
                 camera: int = 0) -> None:
        # TODO: Needs to be dynamically found
        self.capture: VideoCapture = cv2.VideoCapture(camera)
        self.calibration_points: list[Point] = calibration_points
        self.sorted_calibration_points: list[Point] = self.sort_calibration_points()
        self.frame: ndarray = self.update_frame()
        self.height: int = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width: int = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.name: str = name
        self.ptm: Optional[ndarray] = None
        self.warped_width: Optional[int] = None
        self.warped_height: Optional[int] = None
        self.draw_area: DrawArea = draw_area
        self.canvas: Canvas = canvas

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

    def update_frame(self) -> Optional[ndarray]:
        """
        Retrieves the next frame from the camera input and, if successful, returns that.

        :return: An ndarray representing the next frame from the camera input
        """
        success, self.frame = self.capture.read()
        self.frame = cv2.flip(self.frame, 1)
        if success:
            return self.frame
        return None

    def mouse_click(self, event, x, y, flags, param) -> None:
        """
        Sets the calibration points from the x and y position of the mouse.
        If 4 are set, an additional left click of the mouse will clear them.

        :param event: An object containing the type of the event
        :param x: The x position of the mouse
        :param y: The y position of the mouse
        :param flags: Currently unused
        :param param: Currently unused
        """
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
        """
        Draws the calibration points as circles on the camera window.
        """
        for point in self.calibration_points:
            cv2.circle(self.frame, (int(point.x), int(point.y)), int(int(10 / 2) * 2),
                       [255, 255, 0], cv2.FILLED)

    @staticmethod
    def return_camera_indexes() -> List[int]:
        """
        Checks the 20 first camera devices, and if they are live, adds them to a list of usable cameras.

        :return: A list of the indexes for the live cameras
        """
        arr: list[int] = []
        # Checks the first 20 indexes.
        for index in range(20):
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
        return arr

    def update_image_ptm(self) -> None:
        # TODO: Write docstring for method
        if len(self.calibration_points) <= 3:
            None
        else:
            self.ptm, self.warped_width, self.warped_height = fpt(self.frame, self.sorted_calibration_points,
                                                                  self.canvas.width, self.canvas.height)

    def sort_calibration_points(self) -> List[Point]:
        """
        Sorts the list of calibration points using the following order:
        top left, top right, bottom left, bottom right.

        :return: A list of the sorted calibration points
        """
        right_points: list[Point] = []
        left_top: Point = self.calibration_points[0]
        left_bot: Point = self.calibration_points[1]
        for point in self.calibration_points[2:]:
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

        right_top: Point = right_points[0]
        right_bot: Point = right_points[1]

        if left_top.y > left_bot.y:
            temp = left_top
            left_top = left_bot
            left_bot = temp

        if right_top.y > right_bot.y:
            temp = right_top
            right_top = right_bot
            right_bot = temp

        return [left_top, right_top, left_bot, right_bot]
