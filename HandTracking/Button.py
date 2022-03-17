from HandTracking.Point import Point


class Button:
    def __init__(self, callback):
        self.size: int = 25
        self.location: Point = Point(0, 0)
        self.callback = callback
