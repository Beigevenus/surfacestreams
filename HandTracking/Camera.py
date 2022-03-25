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
        self.boundary_points: list[Point] = []
        self.boudaries: dict[str, Optional[int]] = {"x_min": None, "x_max": None, "y_min": None, "y_max": None}

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
                self.frame = cv2.warpPerspective(self.frame, self.ptm, (self.wwidth, self.wheight),
                                                 flags=cv2.INTER_LINEAR)
            return self.frame
        return None

    def update_calibration_point(self, point: Point, width: int, height: int) -> None:
        # TODO: Write docstring for method
        if len(self.calibration_points) > 3:
            if len(self.boundary_points) == 0:
                self.boundary_points.append(point)
            elif len(self.boundary_points) == 1:
                self.boundary_points.append(point)
                min_x = min(self.boundary_points[0].x, self.boundary_points[1].x)
                min_y = min(self.boundary_points[0].y, self.boundary_points[1].y)
                max_x = max(self.boundary_points[0].x, self.boundary_points[1].x)
                max_y = max(self.boundary_points[0].y, self.boundary_points[1].y)

                self.boudaries["x_min"] = int(min_x)
                self.boudaries["y_min"] = int(min_y)
                self.boudaries["x_max"] = int(max_x)
                self.boudaries["y_max"] = int(max_y)

                print(self.boudaries)
            else:
                self.calibration_points.clear()
                self.boundary_points.clear()
                self.boudaries["x_min"] = None
                self.boudaries["y_min"] = None
                self.boudaries["x_max"] = None
                self.boudaries["y_max"] = None
        elif len(self.calibration_points) == 3:
            self.calibration_points.append(point)
            self.sorted_calibration_points = self.sort_calibration_points()
            self.update_image_ptm(width, height)
            Config.save_calibration_points(self.calibration_points)
        else:
            self.calibration_points.append(point)

    def normalise_in_boundary(self, point):
        if self.boudaries["x_max"] is not None:
            x_max: int = self.boudaries["x_max"]
            x_min: int = self.boudaries["x_min"]
            y_max: int = self.boudaries["y_max"]
            y_min: int = self.boudaries["y_min"]
            point_x = point.x * self.wwidth
            point_y = point.y * self.wheight
            if x_max >= point_x >= x_min and y_max >= point_y >= y_min:
                return Point((point_x - x_min) / (x_max - x_min), (point_y - y_min) / (y_max - y_min))

        return None

    def draw_calibration_points(self) -> None:
        """
        Draws the calibration points as circles on the camera window.
        """
        if len(self.calibration_points) < 4:
            for point in self.calibration_points:
                cv2.circle(self.frame, (int(point.x), int(point.y)), int(int(10 / 2) * 2),
                           [255, 255, 0], cv2.FILLED)
        elif len(self.boundary_points) == 1:
            cv2.circle(self.frame, (int(self.boundary_points[0].x), int(self.boundary_points[0].y)),
                       int(int(10 / 2) * 2),
                       [255, 255, 0], cv2.FILLED)
        elif len(self.boundary_points) == 2:
            cv2.rectangle(self.frame, (self.boudaries["x_min"], self.boudaries["y_min"]),
                          (self.boudaries["x_max"], self.boudaries["y_max"]),
                          [255, 255, 0], 10)

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
            self.ptm, self.wwidth, self.wheight = fpt(self.get_expanded_corners(), width, height)

    def get_expanded_corners(self):
        min_x = min(self.sorted_calibration_points[0].x, self.sorted_calibration_points[3].x)
        min_y = min(self.sorted_calibration_points[0].y, self.sorted_calibration_points[1].y)
        max_x = max(self.sorted_calibration_points[1].x, self.sorted_calibration_points[2].x)
        max_y = max(self.sorted_calibration_points[2].y, self.sorted_calibration_points[3].y)

        inner_width = max_x - min_x
        inner_height = max_y - min_y

        aspect_ratio_inner = inner_width / inner_height
        aspect_ratio_outer = self.width / self.height

        if aspect_ratio_outer > aspect_ratio_inner:
            target_aspect = (inner_width * (self.height / inner_height), self.height)
            step_width = (target_aspect[0] - inner_width) / 2
            if min_x - step_width > 0:
                step_width = min_x - step_width
            else:
                step_width = 0
            step_height = 0
        else:
            target_aspect = (self.width, inner_height * (self.width / inner_width))
            step_width = 0
            step_height = (target_aspect[1] - inner_height) / 2
            if min_y - step_height > 0:
                step_height = min_y - step_height
            else:
                step_height = 0

        rel_top_left = Point(
            ((self.sorted_calibration_points[0].x - min_x) / inner_width) * target_aspect[0] + step_width,
            ((self.sorted_calibration_points[0].y - min_y) / inner_height) * target_aspect[1] + step_height)
        rel_top_right = Point(
            ((self.sorted_calibration_points[1].x - min_x) / inner_width) * target_aspect[0] + step_width,
            ((self.sorted_calibration_points[1].y - min_y) / inner_height) * target_aspect[1] + step_height)
        rel_bot_left = Point(
            ((self.sorted_calibration_points[3].x - min_x) / inner_width) * target_aspect[0] + step_width,
            ((self.sorted_calibration_points[3].y - min_y) / inner_height) * target_aspect[1] + step_height)
        rel_bot_right = Point(
            ((self.sorted_calibration_points[2].x - min_x) / inner_width) * target_aspect[0] + step_width,
            ((self.sorted_calibration_points[2].y - min_y) / inner_height) * target_aspect[1] + step_height)

        print(rel_top_left, rel_top_right, rel_bot_right, rel_bot_left)

        return [rel_top_left, rel_top_right, rel_bot_right, rel_bot_left]

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
