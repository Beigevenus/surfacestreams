class PaintingToolbox:
    def __init__(self, size=5, color=None):
        if color is None:
            color = {}
            color['WHITE'] = [150, 150, 150, 255]
            color['BLACK'] = [1, 1, 1, 1]
            color['RED'] = [0, 0, 255, 255]
            color['GREEN'] = [0, 255, 0, 255]

        self.line_size: int = int(size)
        self.circle_size: int = int(size/2)
        self.color: dict = color
        self.mask_circle_radius: int = int(size * 12)
