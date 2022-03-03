class PaintingToolbox:
    def __init__(self, size=10, color=None):
        if color is None:
            color = [120, 0, 120]
        self.line_size: int = int(size)
        self.circle_size: int = int(size/2)
        self.color: list = color
