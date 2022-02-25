from HandTracking.DrawArea import DrawArea
from HandTracking.Point import Point
import pytest

x_fail = pytest.mark.xfail


class Test:
    def test_init_sort(self):
        point1 = Point(10, 11)
        point2 = Point(50, 0)
        point3 = Point(70, 85)
        point4 = Point(20, 120)

        drawarea = DrawArea([point1, point2, point3, point4])
        assert drawarea.sorted_calibration_points == [point1, point2, point4, point3]

    def test_init_sort(self):
        point1 = Point(10, 11)
        point2 = Point(50, 0)
        point3 = Point(70, 85)
        point4 = Point(20, 120)
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



