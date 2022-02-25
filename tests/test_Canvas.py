from HandTracking.Canvas import Canvas
import pytest

x_fail = pytest.mark.xfail


class TestCanvas:
    def test_resize_negative_raises_value_error(self):
        # Arrange
        canvas = Canvas()

        # Act & Assert
        with pytest.raises(ValueError):
            canvas.resize(-1920, 1080)

    def test_resize_zero_raises_value_error(self):
        # Arrange
        canvas = Canvas()

        # Act & Assert
        with pytest.raises(ValueError):
            canvas.resize(0, 1080)

    def test_resize_positive_successful(self):
        # Arrange
        canvas1 = Canvas()
        canvas2 = Canvas()
        canvas3 = Canvas()

        # Act
        canvas1.resize(1280, 720)
        canvas2.resize(1920, 1080)
        canvas3.resize(3840, 2160)

        # Assert
        assert canvas1.width == 1280
        assert canvas1.height == 720
        assert canvas2.width == 1920
        assert canvas2.height == 1080
        assert canvas3.width == 3840
        assert canvas3.height == 2160
