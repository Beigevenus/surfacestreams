from typing import cast
from unittest.mock import patch

from HandTracking.Camera import Camera
from HandTracking.Canvas import Canvas
from HandTracking.DrawArea import DrawArea
from HandTracking.Point import Point
import pytest

x_fail = pytest.mark.xfail


class TestCamera:
    @pytest.mark.parametrize('point1, point2, point3, point4, expected_order',
                             [(Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85)]),
                              (Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85),
                               [Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85)]),
                              (Point(10, 11), Point(70, 85), Point(50, 0), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85)]),
                              (Point(10, 11), Point(70, 85), Point(20, 120), Point(50, 0),
                               [Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85)]),
                              (Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85)]),
                              (Point(20, 120), Point(10, 11), Point(50, 0), Point(70, 85),
                               [Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85)]),
                              (Point(10, 11), Point(70, 85), Point(50, 0), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85)])
                              ])
    @patch.object(Camera, "__init__", lambda obj, draw_area, canvas, cal_points: None)
    def test_sort_calibration_points(self, point1: Point, point2: Point, point3: Point, point4: Point,
                                     expected_order: list[Point]):
        # Arrange
        calibration_points: list[Point] = [point1, point2, point3, point4]
        camera: Camera = Camera(cast(DrawArea, None), cast(Canvas, None), cast(list[Point], None))
        camera.calibration_points = calibration_points

        # Act
        camera.sorted_calibration_points = camera.sort_calibration_points()

        # Assert
        assert camera.sorted_calibration_points[0] == expected_order[0]
        assert camera.sorted_calibration_points[1] == expected_order[1]
        assert camera.sorted_calibration_points[2] == expected_order[2]
        assert camera.sorted_calibration_points[3] == expected_order[3]
