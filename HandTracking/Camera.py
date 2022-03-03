from HandTracking.Point import Point

import cv2


class Camera:
    def __init__(self, name='camera', camera=0) -> None:
        # TODO: Needs to be dynamically found
        self.capture = cv2.VideoCapture(camera)
        self.frame = self.update_frame()
        self.height: int = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width: int = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.name: str = name
        self.calibration_points: list = []

        cv2.namedWindow(self.name)
        cv2.setMouseCallback(self.name, self.mouse_click)

    def show_frame(self) -> None:
        """
        Shows the current camera frame in its window.
        """
        self.draw_calibration_points()
        cv2.imshow(self.name, self.frame)

    def update_frame(self):
        success, self.frame = self.capture.read()
        self.frame = cv2.flip(self.frame, 1)
        if success:
            return self.frame
        return None

    def mouse_click(self, event, x, y, flags, param) -> None:
        if event == cv2.EVENT_LBUTTONUP:
            if len(self.calibration_points) > 3:
                self.calibration_points.clear()
                print("Work!")
            else:
                self.calibration_points.append(Point(x, y))

    def draw_calibration_points(self) -> None:
        for point in self.calibration_points:
            cv2.circle(self.frame, (int(point.x), int(point.y)), int(int(10 / 2) * 2),
                       [255, 255, 0], cv2.FILLED)
