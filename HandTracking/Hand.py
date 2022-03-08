import math

from HandTracking.Point import Point
from HandTracking.Vector import Vector


class Hand:
    def __init__(self, mp_hand):
        self.mp_hand = mp_hand
        self.wrist = None
        self.fingers = {"THUMB": self.Finger(),
                        "INDEX_FINGER": self.Finger(),
                        "MIDDLE_FINGER": self.Finger(),
                        "RING_FINGER": self.Finger(),
                        "PINKY": self.Finger()}

    def update(self, landmarks) -> None:
        """
        TO BE WRITTEN.

        :param landmarks:
        """
        self.wrist = Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark.WRIST])
        # TODO: Make thumb great again
        for key in self.fingers.keys():
            if key == "THUMB":
                self.fingers["THUMB"].update_finger(Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_CMC"]]),
                                                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_MCP"]]),
                                                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_IP"]]),
                                                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_TIP"]]),
                                                    self.wrist)
            else:
                self.fingers[key].update_finger(Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_MCP"]]),
                                                Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_PIP"]]),
                                                Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_DIP"]]),
                                                Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_TIP"]]),
                                                self.wrist)

        # self.calc_distances()

    def calc_distances(self) -> None:
        """
        TO BE WRITTEN.
        """
        for finger in self.fingers.values():
            finger.distance_to_wrist = self.wrist.distance_to(finger.tip)

    def set_finger_length(self) -> None:
        """
        TO BE WRITTEN.
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
        one_extra = False
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
    
    def is_erasing(self) -> bool:
        """
        Determines whether the hand is in 'erasing mode' or not, depending on the position of the fingers.
        Drawing mode is defined as a stretched index, middle and ring finger, with the pinky not stretched.

        :return: Whether the hand is erasing or not
        """
        # TODO: Optimize. we ignore thumb for now
        for key, finger in self.fingers.items():
            if key == "THUMB":
                if not finger.is_stretched():
                    return False
            else:
                if finger.is_stretched():
                    return False
        return True

    def get_drawing_point(self) -> Point:
        """
        Returns the position of the part of the hand that is used for drawing.
        Currently, this is the tip of the index finger.

        :return: The Point that is used for drawing
        """
        return self.fingers["INDEX_FINGER"].tip

    def get_erasing_point(self) -> bool:
        """
        Returns the position of the the tip of the thumb, currently used
        for simple erasing, before the utilization of a ML model to 
        recognize positions and gestures

        :return: The Point that is used for erasing
        """
        return self.fingers["THUMB"].tip

    def get_mask_points(self) -> list:
        points = []

        for finger in self.fingers.values():
            points.append(finger.mcp)
            points.append(finger.pip)
            points.append(finger.dip)

        points.append(self.wrist)
        return points

    class Finger:
        def __init__(self, mcp=None, pip=None, dip=None, tip=None, wrist=None):
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

            a = Vector(self.tip, self.pip)
            b = Vector(self.pip, self.wrist)
            angle = a.angle_between(b)
            if angle > 0:
                return True
            return False

        def update_finger(self, mcp=None, pip=None, dip=None, tip=None, wrist=None):
            self.mcp: Point = mcp
            self.pip: Point = pip
            self.dip: Point = dip
            self.tip: Point = tip
            self.wrist: Point = wrist
