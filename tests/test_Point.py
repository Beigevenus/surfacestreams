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
