from Point import Point
from image_wrap import four_point_transform as fpt

import cv2


class Camera:
    def __init__(self, name='camera', camera=0):
        # TODO: Needs to be dynamically found
        self.capture = cv2.VideoCapture(camera)
        self.frame = self.update_frame()
        self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.name = name
        self.calibration_points = []
        self.ptm = None
        self.warped_width = None
        self.warped_height = None

        cv2.namedWindow(self.name)
        cv2.setMouseCallback(self.name, self.mouse_click)

    def show_frame(self):
        self.draw_calibration_points()
        cv2.imshow(self.name, self.frame)

    def update_frame(self):
        success, self.frame = self.capture.read()
        self.frame = cv2.flip(self.frame, 1)
        if success:
            self.update_image_ptm()
            return self.frame
        return None

    def mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            if len(self.calibration_points) > 3:
                self.calibration_points.clear()
            else:
                self.calibration_points.append(Point(x, y))

    def draw_calibration_points(self):
        for point in self.calibration_points:
            cv2.circle(self.frame, (int(point.x), int(point.y)), int(int(10 / 2) * 2),
                       [255, 255, 0], cv2.FILLED)

    def update_image_ptm(self):
        self.ptm, self.warped_width, self.warped_height = fpt(self.frame, self.calibration_points)
