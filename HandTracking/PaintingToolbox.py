class PaintingToolbox:
    def __init__(self, size=5, color=None, mask_color=None):
        if color is None:
            color = [150, 150, 150, 255]
        if mask_color is None:
            mask_color = [1, 1, 1, 1]

        self.line_size: int = int(size)
        self.circle_size: int = int(size/2)
        self.color: list = color
        self.mask_color: list = mask_color
        self.mask_circle: int = int(size*12)
