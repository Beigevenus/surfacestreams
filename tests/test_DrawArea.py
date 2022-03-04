from HandTracking.DrawArea import DrawArea
from HandTracking.Point import Point
import pytest

x_fail = pytest.mark.xfail


class Test:
    def test_borders(self):
        point1 = Point(10, 11)
        point2 = Point(50, 0)
        point3 = Point(20, 120)
        point4 = Point(70, 85)
        expected_leftborder = [10.9, -98]
        expected_topborder = [-0.275, 13.75]
        expected_rightborder = [4.25, -212.5]
        expected_bottomborder = [-0.7, 134]

        drawarea = DrawArea([point1, point2, point3, point4])

        assert drawarea.left_border[0] == expected_leftborder[0]
        assert drawarea.left_border[1] == expected_leftborder[1]
        assert drawarea.top_border[0] == expected_topborder[0]
        assert drawarea.top_border[1] == expected_topborder[1]
        assert drawarea.right_border[0] == expected_rightborder[0]
        assert drawarea.right_border[1] == expected_rightborder[1]
        assert drawarea.bottom_border[0] == expected_bottomborder[0]
        assert drawarea.bottom_border[1] == expected_bottomborder[1]

    def test_is_position_in_calibration_area_for_vertical_borders(self):
        point1 = Point(0, 0)
        point2 = Point(30, 0)
        point3 = Point(0, 30)
        point4 = Point(30, 30)
        test_pont = Point(20, 20)

        drawarea = DrawArea([point1, point2, point3, point4])

        assert drawarea.left_border[0] is None
        assert drawarea.right_border[0] is None
        assert drawarea.is_position_in_calibration_area(test_pont) is True

    @pytest.mark.parametrize('point', [(Point(20, 10)),
                                                 (Point(18, 9)),
                                                 (Point(60, 70)),
                                                 (Point(20, 54)),
                                                 (Point(40, 35)),
                                                 (Point(14, 17))
                                                 ])
    def test_is_position_in_calibration_area_when_inside(self, point):
        point1 = Point(10, 11)
        point2 = Point(50, 0)
        point3 = Point(20, 120)
        point4 = Point(70, 85)

        drawarea = DrawArea([point1, point2, point3, point4])

        assert drawarea.is_position_in_calibration_area(point) is True

    @pytest.mark.parametrize('point', [(Point(17, 8)),
                                                 (Point(-10, 5)),
                                                 (Point(90, 80)),
                                                 (Point(110, 20)),
                                                 (Point(5, 5))
                                                 ])
    def test_is_position_in_calibration_area_when_outside(self, point):
        point1 = Point(10, 11)
        point2 = Point(50, 0)
        point3 = Point(70, 85)
        point4 = Point(20, 120)

        drawarea = DrawArea([point1, point2, point3, point4])

        assert drawarea.is_position_in_calibration_area(point) is False


