from Point import Point


class Hand:
    def __init__(self, mp_hand):
        self.mp_hand = mp_hand
        self.wrist = None
        self.fingers = {"THUMB": self.Finger(),
                        "INDEX": self.Finger(),
                        "MIDDLE": self.Finger(),
                        "RING": self.Finger(),
                        "PINKY": self.Finger()}

    def update(self, landmarks) -> None:
        """
        TO BE WRITTEN.

        :param landmarks:
        """
        self.wrist = Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark.WRIST])
        self.fingers["THUMB"].tip = Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark.THUMB_TIP])
        self.fingers["INDEX"].tip = Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark.INDEX_FINGER_TIP])
        self.fingers["MIDDLE"].tip = Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark.MIDDLE_FINGER_TIP])
        self.fingers["RING"].tip = Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark.RING_FINGER_TIP])
        self.fingers["PINKY"].tip = Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark.PINKY_TIP])
        self.calc_distances()

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
        for key, finger in self.fingers.items():
            if key == "INDEX":
                if not finger.is_stretched():
                    return False
            elif key == "THUMB":
                None
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
        return self.fingers["INDEX"].tip

    class Finger:
        def __init__(self, mcp=None, pip=None, dip=None, tip=None):
            self.mcp: Point = mcp
            self.pip: Point = pip
            self.dip: Point = dip
            self.tip: Point = tip
            self.distance_to_wrist: float = 0
            self.length: float = 0
            self.stretched_guard: float = 0

        def is_stretched(self) -> bool:
            """
            Determines whether a finger is stretched or not.

            :return: Whether the finger is stretched or not
            """
            return self.stretched_guard < self.distance_to_wrist
