import cv2
import numpy as np

from PaintingToolbox import PaintingToolbox


class Canvas:
    def __init__(self, width=1920, height=1080, toolbox=PaintingToolbox()):
        self.width = width
        self.height = height
        self.toolbox = toolbox
        self.image = np.zeros(shape=[height, width, 3], dtype=np.uint8)

    def resize(self, width, height):
        # Update the screen resolution to fit the computer screen
        # TODO: Make the damn drawing work
        self.image = cv2.resize(self.image, (width, height), interpolation=cv2.INTER_AREA)
        self.width = width
        self.height = height

    def draw(self, previous_point, point):
        cv2.circle(self.image, (int(point.x), int(point.y)),
                   int(self.toolbox.circle_size), self.toolbox.color, cv2.FILLED)

        # Draws line between old index finger tip position, and actual position
        cv2.line(self.image, (int(previous_point.x), int(previous_point.y)),
                 (int(point.x), int(point.y)),
                 self.toolbox.color, self.toolbox.line_size)
