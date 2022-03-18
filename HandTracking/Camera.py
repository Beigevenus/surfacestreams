from typing import Optional

import numpy as np
from cv2 import VideoCapture
from numpy import ndarray

from HandTracking.Config import Config
from HandTracking.Point import Point
from HandTracking.image_wrap import four_point_transform as fpt

import cv2


class Camera:
    def __init__(self, calibration_points: list[Point], name: str = 'camera', camera: int = 0) -> None:
        # TODO: Needs to be dynamically found
        self.capture: VideoCapture = cv2.VideoCapture(camera)
        self.calibration_points: list[Point] = calibration_points
        self.sorted_calibration_points: list[Point] = self.sort_calibration_points()
        self.ptm: Optional[ndarray] = None
        self.wwidth = 0
        self.wheight = 0
        self.frame: ndarray = self.update_frame()
        self.height: int = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width: int = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.name: str = name

        cv2.namedWindow(self.name)

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
            if self.ptm is not None and len(self.calibration_points) > 3:
                self.frame = cv2.warpPerspective(self.frame, self.ptm, (self.wwidth, self.wheight), flags=cv2.INTER_LINEAR)
                self.frame = cv2.resize(self.frame, (1200, 600))
            return self.frame
        return None

    def update_calibration_point(self, point: Point, width: int, height: int) -> None:
        # TODO: Write docstring for method
        if len(self.calibration_points) > 3:
            self.calibration_points.clear()
        elif len(self.calibration_points) == 3:
            self.calibration_points.append(point)
            self.sorted_calibration_points = self.sort_calibration_points()
            self.update_image_ptm(width, height)
            Config.save_calibration_points(self.calibration_points)
        else:
            self.calibration_points.append(point)

    def draw_calibration_points(self) -> None:
        """
        Draws the calibration points as circles on the camera window.
        """
        for point in self.calibration_points:
            cv2.circle(self.frame, (int(point.x), int(point.y)), int(int(10 / 2) * 2),
                       [255, 255, 0], cv2.FILLED)

    @staticmethod
    def return_camera_indexes() -> list[int]:
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

    def update_image_ptm(self, width: int, height: int) -> None:
        # TODO: Write docstring for method
        if not len(self.calibration_points) <= 3:
            self.ptm, self.wwidth, self.wheight = fpt(self.sorted_calibration_points, width, height)

    def sort_calibration_points(self) -> list[Point]:
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

        return [left_top, right_top, right_bot, left_bot]

    def transform_point(self, point, width, height):
        # TODO: Write docstring for method
        # corrected_coordinates = np.matmul(self.ptm, [point.x, point.y, 1])

        return Point(round((point.x) * width), round((point.y) * height))

    def convert_point_to_res(self, point: Point):
        # TODO: If needed add limit and round to the x and y
        # TODO: Add docstring
        return Point(point.x * self.width, point.y * self.height)

    def calibration_is_done(self):
        return len(self.calibration_points) > 3
