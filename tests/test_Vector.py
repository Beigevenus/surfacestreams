from HandTracking.Point import Point
import pytest

from HandTracking.Vector import Vector

x_fail = pytest.mark.xfail


class TestVector:
    @pytest.mark.parametrize("start_p_1, end_p_1, start_p_2, end_p_2, expected_dot",
                             [(Point(0, 3), Point(7, 8), Point(-2, 0), Point(7, -2), 53),
                              (Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0), 0),
                              (Point(-35, -96), Point(-49, -79), Point(34, -93), Point(26, -92), 129),
                              (Point(-6, -64), Point(-43, -96), Point(95, -39), Point(96, -17), -741)])
    def test_dot(self, start_p_1, end_p_1, start_p_2, end_p_2, expected_dot):
        # Arrange
        vector1: Vector = Vector(start_p_1, end_p_1)
        vector2: Vector = Vector(start_p_2, end_p_2)

        # Act
        dot_product: float = vector1.dot(vector2)

        # Assert
        assert dot_product == expected_dot

    # TODO: Fix the expected angles to match what we actually expect
    # @pytest.mark.parametrize("start_p_1, end_p_1, start_p_2, end_p_2, expected_angle",
    #                          [(Point(0, 3), Point(7, 8), Point(-2, 0), Point(7, -2), 48.0664),
    #                           (Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0), 0),
    #                           (Point(-35, -96), Point(-49, -79), Point(34, -93), Point(26, -92), 43.4025),
    #                           (Point(-6, -64), Point(-43, -96), Point(95, -39), Point(96, -17), 46.5421)])
    # def test_angle_between(self, start_p_1, end_p_1, start_p_2, end_p_2, expected_angle):
    #     # Arrange
    #     vector1: Vector = Vector(start_p_1, end_p_1)
    #     vector2: Vector = Vector(start_p_2, end_p_2)
    #
    #     # Act
    #     angle: float = vector1.angle_between(vector2)
    #
    #     # Assert
    #     assert round(angle, 4) == expected_angle
