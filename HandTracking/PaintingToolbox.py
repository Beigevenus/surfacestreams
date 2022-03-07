class PaintingToolbox:
    def __init__(self, size=5, color=None):
        if color is None:
            color = [150, 150, 150]
        self.line_size: int = int(size)
        self.circle_size: int = int(size/2)
        self.color: list = color
