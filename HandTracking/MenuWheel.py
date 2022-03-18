from HandTracking.Button import Button
from HandTracking.Layer import Layer
from HandTracking.Point import Point


class MenuWheel:
    def __init__(self, layer: Layer, drawing_layer: Layer):
        self.is_open: bool = False
        self.tool_buttons: list[Button] = []
        self.color_buttons: list[Button] = []
        self.layer = layer
        self.center_point = Point(0, 0)
        self.drawing_layer = drawing_layer

        self.initialize_buttons()

    def initialize_buttons(self):
        self.add_tool_button(self.__select_eraser)
        self.add_tool_button(self.__select_drawer)
        self.add_tool_button(self.__select_color_wheel)

        for color in self.drawing_layer.toolbox.color_palette:
            print(color)
            self.add_color_button(self.__change_color, color)

    def open(self):
        pass

    def add_tool_button(self, callback):
        self.tool_buttons.append(Button(callback))

    def add_color_button(self, callback, color):
        self.color_buttons.append(Button(callback, color=color))

    def draw_buttons(self):
        self.layer.toolbox.circle_size = round(self.layer.width*0.03)
        self.layer.toolbox.change_color("WHITE")
        bot_left = Point(self.layer.width, self.layer.height)
        circle_size = self.layer.toolbox.circle_size
        for idx, button in enumerate(self.tool_buttons):
            button_location = Point(round(bot_left.x-circle_size-(circle_size/2)), round(bot_left.y-((circle_size*2+10)*(idx+1))-(circle_size*2)))
            button.set_location(button_location)
            self.layer.draw_circle(button.location)

        for idx, button in enumerate(self.color_buttons):
            button_location = Point(round(bot_left.x-((circle_size*2+10)*(idx+1))-(circle_size*2)), round(bot_left.y-circle_size-(circle_size/2)))
            self.layer.toolbox.change_color(button.color)
            button.set_location(button_location)
            self.layer.draw_circle(button.location)


    def __select_eraser(self):
        print('selected: Eraser')

    def __select_drawer(self):
        print('selected: Draw')

    def __select_color_wheel(self):
        print('selected: Color')

    def __change_color(self):
        print('selected: a color like red maybe?')

    def open_menu(self):
        self.is_open = True
        self.draw_buttons()
        pass

    def close_menu(self):
        self.is_open = False
        self.layer.wipe()
        pass

