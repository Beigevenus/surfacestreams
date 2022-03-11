from HandTracking.Point import Point
import pytest

x_fail = pytest.mark.xfail


class TestPoint:
    @pytest.mark.parametrize("x1, y1, x2, y2, expected_distance", [(10, 23, 13, 7, 16.2788),
                                                                   (10, 23, 2, -5, 29.1204),
                                                                   (10, 23, -32, 0, 47.8853),
                                                                   (13, 7, 2, -5, 16.2788),
                                                                   (13, 7, -32, 0, 45.5412),
                                                                   (2, -5, -32, 0, 34.3657)])
    def test_distance_to(self, x1, y1, x2, y2, expected_distance):
        # Arrange
        point1: Point = Point(x1, y1)
        point2: Point = Point(x2, y2)

        # Act
        distance: float = point1.distance_to(point2)

        # Assert
        assert round(distance, 4) == expected_distance

    @pytest.mark.parametrize("x, y, area_width, area_height, canvas_width, canvas_height, expected_x, expected_y",
                             [(30, 65, 1280, 720, 1920, 1080, 45.0000, 97.5000),
                              (8, 3, 600, 400, 1280, 720, 17.0667, 5.4000),
                              (-14, 52, 3840, 2160, 2560, 1440, -9.3333, 34.6667)])
    def test_get_position_on_canvas(self, x, y, area_width, area_height, canvas_width, canvas_height, expected_x,
                                    expected_y):
        # Arrange
        point: Point = Point(x, y)

        # Act
        actual: Point = point.get_position_on_canvas(area_width, area_height, canvas_width, canvas_height)

        # Assert
        assert round(actual.x, 4) == expected_x
        assert round(actual.y, 4) == expected_y

    @pytest.mark.parametrize("area_width, area_height, canvas_width, canvas_height", [(0, 720, 1920, 1080),
                                                                                      (1280, 0, 1920, 1080),
                                                                                      (1280, 720, 0, 1080),
                                                                                      (1280, 720, 1920, 0)])
    def test_get_position_on_canvas_raises_zero_division_error(self, area_width, area_height, canvas_width,
                                                               canvas_height):
        # Arrange
        point: Point = Point(40, 60)

        # Act & Assert
        with pytest.raises(ZeroDivisionError):
            point.get_position_on_canvas(area_width, area_height, canvas_width, canvas_height)
