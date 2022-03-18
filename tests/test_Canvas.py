import numpy as np

from HandTracking.Canvas import Canvas
import pytest

from HandTracking.PaintingToolbox import PaintingToolbox

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
        canvas.layers = []

        # Act
        canvas.resize(width, height)

        # Assert
        assert canvas.width == expected_width
        assert canvas.height == expected_height

    @pytest.mark.parametrize("name, position, expected_position", [("TEST1", 0, 0),
                                                                   ("TEST2", 1, 1),
                                                                   ("TEST3", -1, -1),
                                                                   ("TEST4", 35, 3),
                                                                   ("TEST5", 2, 2)])
    def test_create_layer(self, name, position, expected_position):
        # Arrange
        canvas: Canvas = Canvas.__new__(Canvas)
        canvas.layers = [(), (), ()]
        canvas.width = 100
        canvas.height = 100
        toolbox: PaintingToolbox = PaintingToolbox()

        # Act
        canvas.create_layer(name, toolbox, position)

        # Assert
        assert canvas.layers[expected_position][0] == name

    # TODO: Write test case
    def test_delete_layer(self):
        pass

    # TODO: Write test case
    @pytest.mark.parametrize("layer_list", [()])
    def test_get_layer(self, layer_list):
        pass
