import math
from typing import Optional

from HandTracking.Point import Point
from HandTracking.Vector import Vector
from HandTracking.keypoint_classifier.keypoint_classifier import KeyPointClassifier


class Hand:
    def __init__(self, mp_hand) -> None:
        self.mp_hand = mp_hand
        self.wrist: Optional[Point] = None
        self.fingers: dict = {"THUMB": self.Finger(),
                              "INDEX_FINGER": self.Finger(),
                              "MIDDLE_FINGER": self.Finger(),
                              "RING_FINGER": self.Finger(),
                              "PINKY": self.Finger()}
        self.keypoint_classifier = KeyPointClassifier()

    def update(self, landmarks) -> None:
        # TODO: Write docstring for method
        self.wrist = Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark.WRIST])
        # TODO: Make thumb great again
        for key in self.fingers.keys():
            if key == "THUMB":
                self.fingers["THUMB"].update_finger(
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_CMC"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_MCP"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_IP"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_TIP"]]),
                    self.wrist)
            else:
                self.fingers[key].update_finger(
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_MCP"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_PIP"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_DIP"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_TIP"]]),
                    self.wrist)

        # self.calc_distances()

    def calc_distances(self) -> None:
        """
        Calculates the distance from each finger to the wrist and saves them.
        """
        for finger in self.fingers.values():
            finger.distance_to_wrist = self.wrist.distance_to(finger.tip)

    def set_finger_length(self) -> None:
        """
        Sets the length of each finger and their stretched guard.
        """
        for finger in self.fingers.values():
            finger.length = finger.distance_to_wrist
            finger.stretched_guard = 0.9 * finger.length

    def is_drawing(self) -> bool:
        """
        Determines whether the hand is in 'drawing mode' or not, depending on the position of the fingers.
        Drawing mode is defined as a stretched index finger, and all other fingers being bent.

        :return: Whether the hand is drawing or not
        """
        # TODO: Optimize. we ignore thumb for now
        one_extra: bool = False
        for key, finger in self.fingers.items():
            if key == "INDEX_FINGER":
                if not finger.is_stretched():
                    return False
            elif key == "THUMB":
                None
            else:
                if finger.is_stretched():
                    if one_extra:
                        return False
                    else:
                        one_extra = True
        return True

    def get_drawing_point(self) -> Point:
        """
        Returns the position of the part of the hand that is used for drawing.
        Currently, this is the tip of the index finger.

        :return: The Point that is used for drawing
        """
        return self.fingers["INDEX_FINGER"].tip

    def get_mask_points(self) -> list[Point]:
        # TODO: Write docstring for method
        points: list[Point] = []

        for finger in self.fingers.values():
            points.append(finger.mcp)
            points.append(finger.pip)
            points.append(finger.dip)

        points.append(self.wrist)
        return points

    def get_hand_sign(self, camera_frame, landmarks) -> str:
        return self.keypoint_classifier.get_hand_sign(camera_frame, landmarks)

    class Finger:
        def __init__(self, mcp: Point = None, pip: Point = None, dip: Point = None, tip: Point = None,
                     wrist: Point = None):
            self.mcp: Point = mcp
            self.pip: Point = pip
            self.dip: Point = dip
            self.tip: Point = tip
            self.wrist: Point = wrist
            self.distance_to_wrist: float = 0
            self.length: float = 0
            self.stretched_guard: float = 0

        def __str__(self) -> str:
            return f"({self.mcp}, {self.pip}, {self.dip}, {self.tip})"

        def is_stretched(self) -> bool:
            """
            Determines whether a finger is stretched or not.

            :return: Whether the finger is stretched or not
            """
            if self.pip is None or self.mcp is None or self.tip is None:
                return False

            a: Vector = Vector(self.tip, self.pip)
            b: Vector = Vector(self.pip, self.wrist)
            angle: float = a.angle_between(b)
            if angle > 0:
                return True
            return False

        def update_finger(self, mcp: Point = None, pip: Point = None, dip: Point = None, tip: Point = None,
                          wrist: Point = None):
            # TODO: Write docstring for method
            self.mcp = mcp
            self.pip = pip
            self.dip = dip
            self.tip = tip
            self.wrist = wrist
