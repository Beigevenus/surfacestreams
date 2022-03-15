import cv2
import numpy as np
from numpy import ndarray

from HandTracking.PaintingToolbox import PaintingToolbox
from HandTracking.Point import Point


class Canvas:
    def __init__(self, width: int = 1920, height: int = 1080, name: str = 'canvas',
                 toolbox: PaintingToolbox = PaintingToolbox()) -> None:
        self.width: int = width
        self.height: int = height
        self.toolbox: PaintingToolbox = toolbox
        self.image: ndarray = np.zeros(shape=[height, width, 4], dtype=np.uint8)
        self.name: str = name

        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        # self.move_window(2500)

    def resize(self, width: int, height: int) -> None:
        """
        Changes the width and height of the canvas resolution to the given lengths.

        :param width: The desired width
        :param height: The desired height
        """
        if width <= 0 or height <= 0:
            raise ValueError("Width and height of a resized canvas must be larger than 0.")

        self.image = cv2.resize(self.image, (width, height), interpolation=cv2.INTER_AREA)
        self.width = width
        self.height = height

    # TODO: Make it so that the smoothing is an option, so that you can erase with ease
    def draw_line(self, previous_point, point) -> None:

        """
        Draws a circle at the current point, and a line between the old and current point.

        :param previous_point: The start position of the line segment
        :param point: The end position of the line segment
        """
        if previous_point is None:
            previous_point = point

        cv2.circle(self.image, (int(point.x), int(point.y)),
                   int(self.toolbox.circle_size), self.toolbox.current_color, cv2.FILLED)

        # Draws line between old index finger tip position, and actual position
        cv2.line(self.image, (int(previous_point.x), int(previous_point.y)),
                 (int(point.x), int(point.y)),
                 self.toolbox.current_color, self.toolbox.line_size)

    def draw_mask_points(self, points: list[Point], color: str, size: int) -> None:
        """
        Draws mask circles (black circles to cover the hand) at every point given.

        :param points: A list of Point objects to draw mask circles at
        """
        if size is None:
            size = int(self.toolbox.mask_circle_radius)

        for point in points:
            cv2.circle(self.image, (int(point.x), int(point.y)),
                       size, self.toolbox.color[color], cv2.FILLED)

    def show(self) -> None:
        """
        Updates the shown canvas in its window.
        """
        cv2.imshow(self.name, cv2.flip(self.image, 1))
        self.__check_for_resize()

    def __check_for_resize(self) -> None:
        """
        Checks if the dimensions of the canvas window has changed and update its resolution accordingly.
        """
        width: int
        height: int
        width, height = cv2.getWindowImageRect(self.name)[2:]
        if width != self.width or height != self.height:
            self.resize(width, height)

    def fullscreen(self) -> None:
        """
        Switches the canvas window to fullscreen mode.
        """
        cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def move_window(self, offset_x: int, offset_y: int) -> None:
        """
        Moves the canvas window horizontally by the given offset.

        :param offset_x: The number of pixels to move the window in the horizontal plane
        :param offset_y: The number of pixels to move the window in the vertical plane
        """
        cv2.moveWindow(self.name, offset_x, offset_y)
