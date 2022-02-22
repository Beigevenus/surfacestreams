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

    def update(self, landmarks):
        self.wrist = Point(landmarks.landmark[self.mp_hand.HandLandmark.WRIST])
        self.fingers["THUMB"].tip = Point(landmarks.landmark[self.mp_hand.HandLandmark.THUMB_TIP])
        self.fingers["INDEX"].tip = Point(landmarks.landmark[self.mp_hand.HandLandmark.INDEX_FINGER_TIP])
        self.fingers["MIDDLE"].tip = Point(landmarks.landmark[self.mp_hand.HandLandmark.MIDDLE_FINGER_TIP])
        self.fingers["RING"].tip = Point(landmarks.landmark[self.mp_hand.HandLandmark.RING_FINGER_TIP])
        self.fingers["PINKY"].tip = Point(landmarks.landmark[self.mp_hand.HandLandmark.PINKY_TIP])
        self.calc_distances()

    def calc_distances(self):
        for finger in self.fingers.values():
            finger.distance_to_wrist = self.wrist.distance_to(finger.tip)

    def set_finger_length(self):
        for finger in self.fingers.values():
            finger.length = finger.distance_to_wrist
            finger.stretched_guard = 0.9 * finger.length

    def is_drawing(self):
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

    def get_drawing_point(self):
        return self.fingers["INDEX"].tip

    class Finger:
        def __init__(self, mcp=None, pip=None, dip=None, tip=None):
            self.mcp = mcp
            self.pip = pip
            self.dip = dip
            self.tip = tip
            self.distance_to_wrist = 0
            self.length = 0
            self.stretched_guard = 0

        def is_stretched(self):
            return self.stretched_guard < self.distance_to_wrist
