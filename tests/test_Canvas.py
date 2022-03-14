import numpy as np

from HandTracking.Canvas import Canvas
import pytest

x_fail = pytest.mark.xfail


class TestCanvas:
    @pytest.mark.parametrize("width, height", [(-1920, 1080), (1920, -1080)])
    def test_resize_negative_raises_value_error(self, width, height):
        # Arrange
        canvas: Canvas = Canvas.__new__(Canvas)

        # Act & Assert
        with pytest.raises(ValueError):
            canvas.resize(width, height)

    @pytest.mark.parametrize("width, height", [(0, 1080), (1920, 0)])
    def test_resize_zero_raises_value_error(self, width, height):
        # Arrange
        canvas: Canvas = Canvas.__new__(Canvas)

        # Act & Assert
        with pytest.raises(ValueError):
            canvas.resize(width, height)

    @pytest.mark.parametrize("width, height, expected_width, expected_height", [(1280, 720, 1280, 720),
                                                                                (1920, 1080, 1920, 1080),
                                                                                (3840, 2160, 3840, 2160)])
    def test_resize_positive_successful(self, width, height, expected_width, expected_height):
        # Arrange
        canvas: Canvas = Canvas.__new__(Canvas)
        canvas.image = np.zeros(shape=[height, width, 4], dtype=np.uint8)

        # Act
        canvas.resize(width, height)

        # Assert
        assert canvas.width == expected_width
        assert canvas.height == expected_height
