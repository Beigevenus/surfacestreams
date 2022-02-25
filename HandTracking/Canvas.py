import cv2
import numpy as np

from PaintingToolbox import PaintingToolbox


class Canvas:
    def __init__(self, width=1920, height=1080, name='canvas', toolbox=PaintingToolbox()):
        self.width = width
        self.height = height
        self.toolbox = toolbox
        self.image = np.zeros(shape=[height, width, 3], dtype=np.uint8)
        self.name = name

        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        self.move_window(2500)

    def resize(self, width, height):
        self.image = cv2.resize(self.image, (width, height), interpolation=cv2.INTER_AREA)
        self.width = width
        self.height = height

    def draw(self, previous_point, point):
        if previous_point is None:
            previous_point = point

        cv2.circle(self.image, (int(point.x), int(point.y)),
                   int(self.toolbox.circle_size), self.toolbox.color, cv2.FILLED)

        # Draws line between old index finger tip position, and actual position
        cv2.line(self.image, (int(previous_point.x), int(previous_point.y)),
                 (int(point.x), int(point.y)),
                 self.toolbox.color, self.toolbox.line_size)

    def show(self):
        cv2.imshow(self.name, cv2.flip(self.image, 1))
        self.__check_for_resize()

    def __check_for_resize(self):
        width, height = cv2.getWindowImageRect(self.name)[2:]
        if width != self.width or height != self.height:
            self.resize(width, height)

    def fullscreen(self):
        cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def move_window(self, offset):
        cv2.moveWindow(self.name, offset, 0)
