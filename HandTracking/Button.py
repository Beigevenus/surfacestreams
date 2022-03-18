from HandTracking.Point import Point


class Button:
    def __init__(self, callback, color='WHITE'):
        self.size: int = 25
        self.location: Point = Point(0, 0)
        self.callback = callback
        self.selected: bool = False
        self.color = color

    def set_location(self, point: Point):
        self.location = point

