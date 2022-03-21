from HandTracking.Camera import Camera
from HandTracking.Point import Point
import pytest

x_fail = pytest.mark.xfail


class TestCamera:
    @pytest.mark.parametrize('point1, point2, point3, point4, expected_order',
                             [(Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(10, 11), Point(70, 85), Point(50, 0), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(10, 11), Point(70, 85), Point(20, 120), Point(50, 0),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(20, 120), Point(10, 11), Point(50, 0), Point(70, 85),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(10, 11), Point(70, 85), Point(50, 0), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)])
                              ])
    def test_sort_calibration_points(self, point1: Point, point2: Point, point3: Point, point4: Point,
                                     expected_order: list[Point]):
        # Arrange
        calibration_points: list[Point] = [point1, point2, point3, point4]
        camera: Camera = Camera.__new__(Camera)
        camera.calibration_points = calibration_points

        # Act
        camera.sorted_calibration_points = camera.sort_calibration_points()

        # Assert
        assert camera.sorted_calibration_points[0] == expected_order[0]
        assert camera.sorted_calibration_points[1] == expected_order[1]
        assert camera.sorted_calibration_points[2] == expected_order[2]
        assert camera.sorted_calibration_points[3] == expected_order[3]

    # TODO: Write test case
    def test_transform_point(self):
        pass

    @pytest.mark.parametrize("point, expected_point", [(Point(0, 0), Point(0, 0)),
                                                       (Point(32, 7), Point(40960, 5040)),
                                                       (Point(-2, -8), Point(-2560, -5760))])
    def test_convert_point_to_res(self, point, expected_point):
        # Arrange
        camera: Camera = Camera.__new__(Camera)
        camera.width = 1280
        camera.height = 720

        # Act
        actual = camera.convert_point_to_res(point)

        # Assert
        assert actual == expected_point

    @pytest.mark.parametrize("cal_points, expected", [([], False),
                                                      ([Point(0, 0)], False),
                                                      ([Point(0, 0), Point(0, 0)], False),
                                                      ([Point(0, 0), Point(0, 0), Point(0, 0)], False),
                                                      ([Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)], True)])
    def test_calibration_is_done(self, cal_points, expected):
        # Arrange
        camera: Camera = Camera.__new__(Camera)
        camera.calibration_points = cal_points

        # Act
        actual = camera.calibration_is_done()

        # Assert
        assert actual == expected
