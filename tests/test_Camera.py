from HandTracking.DrawArea import DrawArea
from HandTracking.Camera import Camera
from HandTracking.Canvas import Canvas
from HandTracking.Point import Point
import pytest

x_fail = pytest.mark.xfail


class TestCamera:
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
        class Empty(object):
            pass

        calibration_points = [point1, point2, point3, point4]
        camera = Empty()
        camera.__class__ = Camera
        camera.calibration_points = calibration_points
        camera.sorted_calibration_points = camera.sort_calibration_points()
        assert camera.sorted_calibration_points[0].x == 10 and camera.sorted_calibration_points[0].y == 11
        assert camera.sorted_calibration_points[1].x == 50 and camera.sorted_calibration_points[1].y == 0
        assert camera.sorted_calibration_points[2].x == 20 and camera.sorted_calibration_points[2].y == 120
        assert camera.sorted_calibration_points[3].x == 70 and camera.sorted_calibration_points[3].y == 85

