from HandTracking.Button import Button
from HandTracking.Layer import Layer
from HandTracking.Point import Point


class MenuWheel:
    def __init__(self, layer: Layer):
        self.buttons: list[Button] = []
        self.layer = layer

        self.initialize_buttons()

    def initialize_buttons(self):
        self.add_button(self.__select_eraser())
        self.add_button(self.__select_drawer())
        self.add_button(self.__select_color_wheel())

    def open(self):
        pass

    def add_button(self, callback):
        self.buttons.append(Button(callback))

    def draw_buttons(self):
        pass

    def __select_eraser(self):
        print('selected: Eraser')

    def __select_drawer(self):
        print('selected: Draw')

    def __select_color_wheel(self):
        print('selected: Color')
