from typing import Optional

import cv2
import numpy as np
from numpy import ndarray

from HandTracking.Camera import Camera
from HandTracking.Layer import Layer
from HandTracking.PaintingToolbox import PaintingToolbox
from HandTracking.Point import Point


class Canvas:
    def __init__(self, name, width: int = 1920, height: int = 1080) -> None:
        self.width: int = width
        self.height: int = height
        self.name: str = name
        self.layers: list[(str, Layer)] = [("MASK", Layer(width, height, PaintingToolbox(50, current_color="BLACK")))]

        # TODO: Remove when it is no longer necessary
        self.create_layer("CAL_CROSS", PaintingToolbox(5, current_color="BLUE"))

        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        # self.move_window(2500)

    def create_layer(self, name: str, toolbox: PaintingToolbox, position: int = -1) -> None:
        # TODO: Write docstring for method
        if position == -1:
            self.layers.append((name, Layer(self.width, self.height, toolbox)))
        else:
            self.layers.insert(position, (name, Layer(self.width, self.height, toolbox)))

    def delete_layer(self, name: str) -> None:
        # TODO: Write docstring for method
        layer = self.find_layer(name)

        if layer:
            self.layers.remove(layer)

    def get_layer(self, name: str) -> Optional[Layer]:
        # TODO: Write docstring for method
        layer = self.find_layer(name)

        if layer:
            return self.find_layer(name)[1]
        else:
            return None

    def find_layer(self, name: str) -> Optional[tuple[str, Layer]]:
        # TODO: Write docstring for method
        for layer_name, layer in self.layers:
            if name == layer_name:
                return layer_name, layer
        return None

    def combine_layers(self) -> ndarray:
        # TODO: Write docstring for method
        combined_image: ndarray = np.zeros(shape=[self.height, self.width, 4], dtype=np.uint8)

        for name, layer in self.layers[::-1]:
            src_a = layer.image[..., 3] > 0

            combined_image[src_a] = layer.image[src_a]

        return combined_image

    def resize(self, width: int, height: int) -> None:
        """
        Changes the width and height of the canvas resolution and its layers to the given lengths.

        :param width: The desired width
        :param height: The desired height
        """
        if width <= 0 or height <= 0:
            raise ValueError("Width and height of a resized canvas must be larger than 0.")

        for name, layer in self.layers:
            layer.image = cv2.resize(layer.image, (width, height), interpolation=cv2.INTER_AREA)
            layer.width = width
            layer.height = height

        self.width = width
        self.height = height

    def draw_mask_points(self, points: list[Point]) -> None:
        # TODO: Write docstring for method

        for point in points:
            self.get_layer("MASK").draw_circle(point)

    def show(self) -> None:
        """
        Updates the shown canvas in its window.
        """
        cv2.imshow(self.name, cv2.flip(self.combine_layers(), 1))
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

    # TODO: Remove when it is no longer necessary
    def print_calibration_cross(self, camera: Camera):
        print("top left:")
        top_left = camera.transform_point(camera.sorted_calibration_points[0])
        print(int(top_left.x), int(top_left.y))

        print("top right:")
        top_right = camera.transform_point(camera.sorted_calibration_points[1])
        print(int(top_right.x), int(top_right.y))

        print("bot left:")
        bot_left = camera.transform_point(camera.sorted_calibration_points[2])
        print(int(bot_left.x), int(bot_left.y))

        print("bot right:")
        bot_right = camera.transform_point(camera.sorted_calibration_points[3])
        print(int(bot_right.x), int(bot_right.y))

        self.get_layer("CAL_CROSS").wipe()
        self.get_layer("CAL_CROSS").draw_line(top_left, top_right)
        self.get_layer("CAL_CROSS").draw_line(top_right, bot_right)
        self.get_layer("CAL_CROSS").draw_line(bot_right, bot_left)
        self.get_layer("CAL_CROSS").draw_line(bot_left, top_left)
