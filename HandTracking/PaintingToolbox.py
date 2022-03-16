from typing import Optional


class PaintingToolbox:
    def __init__(self, size: int = 5, color: Optional[list[int]] = None) -> None:

        if color is None:
            color = {'WHITE': [150, 150, 150, 255], 'BLACK': [1, 1, 1, 1], 'RED': [0, 0, 255, 255],
                     'GREEN': [0, 255, 0, 255]}

        self.line_size: int = int(size)
        self.circle_size: int = int(size/2)
        self.color: dict = color
        self.mask_circle_radius: int = int(size * 12)
        self.current_color = self.color['WHITE']

    def change_color(self, new_color: str):
        # TODO: Write docstring for method
        try:
            self.current_color = self.color[new_color]
        except KeyError:
            self.current_color = self.color['WHITE']

    def change_color_rgba(self, new_color: list[int]):
        # TODO: Write docstring for method
        self.current_color = new_color

    def change_line_size(self, size: int = 5):
        # TODO: Write docstring for method
        self.line_size = int(size)
        self.circle_size = int(size / 2)
