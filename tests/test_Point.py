from HandTracking.Point import Point
import pytest

x_fail = pytest.mark.xfail


class TestPoint:
    def test_distance_to(self):
        # Arrange
        point1 = Point(10, 23)
        point2 = Point(13, 7)
        point3 = Point(2, -5)
        point4 = Point(-32, 0)

        # Act
        distance1_2 = point1.distance_to(point2)
        distance1_3 = point1.distance_to(point3)
        distance1_4 = point1.distance_to(point4)
        distance2_3 = point2.distance_to(point3)
        distance2_4 = point2.distance_to(point4)
        distance3_4 = point3.distance_to(point4)

        # Assert
        assert round(distance1_2, 4) == 16.2788
        assert round(distance1_3, 4) == 29.1204
        assert round(distance1_4, 4) == 47.8853
        assert round(distance2_3, 4) == 16.2788
        assert round(distance2_4, 4) == 45.5412
        assert round(distance3_4, 4) == 34.3657

    def test_get_position_on_canvas(self):
        pass
