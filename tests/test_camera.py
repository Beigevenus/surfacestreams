from HandTracking.DrawArea import DrawArea
from HandTracking.Camera import Camera
from HandTracking.Point import Point
import pytest

x_fail = pytest.mark.xfail


class Test:
    @pytest.mark.parametrize('point1, point2, point3, point4',
                             [(Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)),
                              (Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85)),
                              (Point(10, 11), Point(70, 85), Point(50, 0), Point(20, 120)),
                              (Point(10, 11), Point(70, 85), Point(20, 120), Point(50, 0)),
                              (Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)),
                              (Point(20, 120), Point(10, 11), Point(50, 0), Point(70, 85)),
                              (Point(10, 11), Point(70, 85), Point(50, 0), Point(20, 120))
                              ])
    def test_init_sort(self, point1, point2, point3, point4):
        calibration_points = [point1, point2, point3, point4]
        drawarea = DrawArea(calibration_points)
        camera = Camera(drawarea, calibration_points)
        assert camera.sorted_calibration_points[0].x == 10 and camera.sorted_calibration_points[0].y == 11
        assert camera.sorted_calibration_points[1].x == 50 and camera.sorted_calibration_points[1].y == 0
        assert camera.sorted_calibration_points[2].x == 20 and camera.sorted_calibration_points[2].y == 120
        assert camera.sorted_calibration_points[3].x == 70 and camera.sorted_calibration_points[3].y == 85

    def test_borders(self):
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

