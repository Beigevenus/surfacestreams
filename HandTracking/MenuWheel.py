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
        self.drawing_color: str = "WHITE"

        self.initialize_buttons()

    def initialize_buttons(self):
        self.add_tool_button(self.__select_eraser)
        self.add_tool_button(self.__select_drawer)
        self.add_tool_button(self.__select_color_wheel)

        for color in self.drawing_layer.color_palette:
            self.add_color_button(self.__change_color, color)

    def open(self):
        pass

    def add_tool_button(self, callback):
        self.tool_buttons.append(Button(callback))

    def add_color_button(self, callback, color):
        if self.drawing_color == color:
            self.color_buttons.append(Button(callback, color=color, active=True))
        else:
            self.color_buttons.append(Button(callback, color=color))

    def draw_buttons(self):
        bot_left = Point(self.layer.width, self.layer.height)
        circle_size = round(self.layer.width * 0.03)

        for idx, button in enumerate(self.tool_buttons):
            button.size = circle_size
            button_location = Point(round(bot_left.x - circle_size - (circle_size / 2)),
                                    round(bot_left.y - ((circle_size * 2 + 10) * (idx + 1)) - (circle_size * 2)))
            button.set_location(button_location)
            
            if button.active:
                self.layer.draw_circle(button.location, "ACTIVE_BLUE", circle_size + 4)

            self.layer.draw_circle(button.location, "WHITE", circle_size)

        for idx, button in enumerate(self.color_buttons):
            button.size = circle_size
            button_location = Point(round(bot_left.x - ((circle_size * 2 + 10) * (idx + 1)) - (circle_size * 2)),
                                    round(bot_left.y - circle_size - (circle_size / 2)))
            button.set_location(button_location)

            if button.active:
                self.layer.draw_circle(button.location, "ACTIVE_BLUE", circle_size + 4)

            self.layer.draw_circle(button.location, button.color, circle_size)

    def __select_eraser(self):
        print('selected: Eraser')

    def __select_drawer(self):
        print('selected: Draw')

    def __select_color_wheel(self):
        print('selected: Color')

    def __change_color(self, button: Button):
        actual_color = self.drawing_layer.color_palette[button.color]

        for button in self.color_buttons:
            if actual_color == self.drawing_layer.color_palette[button.color]:
                button.active = True
                self.drawing_color = button.color
            else:
                button.active = False

    def check_button_click(self, point: Point):
        for button in self.color_buttons:
            if button.is_point_in_circle(point):
                button.callback(button)

    def open_menu(self):
        self.is_open = True
        self.draw_buttons()
        pass

    def close_menu(self):
        self.is_open = False
        self.layer.wipe()
        pass

