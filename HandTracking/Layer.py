import cv2
import numpy as np
from numpy import ndarray

from HandTracking.PaintingToolbox import PaintingToolbox
from HandTracking.Point import Point


class Layer:
    def __init__(self, width: int, height: int, toolbox: PaintingToolbox):
        self.width: int = width
        self.height: int = height
        self.image: ndarray = np.full(shape=[height, width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)
        self.toolbox: PaintingToolbox = toolbox

    def wipe(self) -> None:
        """
        Resets the values of all "pixels" in the layer, making them black.
        """
        self.image: ndarray = np.full(shape=[self.height, self.width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)

    # TODO: Make it so that the smoothing is an option, so that you can erase with ease
    def draw_line(self, previous_point: Point, point: Point) -> None:
        """
        Draws a circle at the current point, and a line between the old and current point.

        :param previous_point: The start position of the line segment
        :param point: The end position of the line segment
        """
        if previous_point is None:
            previous_point = point

        self.draw_circle(point)

        # Draws line between old index finger tip position, and actual position
        cv2.line(self.image, (int(previous_point.x), int(previous_point.y)),
                 (int(point.x), int(point.y)),
                 self.toolbox.current_color, self.toolbox.line_size)

    def draw_circle(self, point: Point) -> None:
        """
        Draws a circle at the specified point's coordinates.

        :param point: The point to draw a circle at
        """
        cv2.circle(self.image, (int(point.x), int(point.y)),
                   self.toolbox.circle_size, self.toolbox.current_color, cv2.FILLED)
