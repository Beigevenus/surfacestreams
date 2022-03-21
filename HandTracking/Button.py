from HandTracking.Point import Point


class Button:
    def __init__(self, callback, color: str = 'WHITE', active: bool = False):
        self.size: int = 25
        self.location: Point = Point(0, 0)
        self.callback = callback
        self.active: bool = active
        self.color = color

    def set_location(self, point: Point):
        self.location = point
