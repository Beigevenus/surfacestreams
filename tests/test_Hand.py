import pytest

from HandTracking.Hand import Hand
from HandTracking.Point import Point

x_fail = pytest.mark.xfail


class TestHand:
    @pytest.mark.parametrize("index_tip", [(Point(0, 0)), (Point(35, 103)), (Point(-82, 7)),
                                           (Point(5, -9)), (Point(7374, -27432))])
    def test_get_index_tip(self, index_tip):
        # Arrange
        hand: Hand = Hand.__new__(Hand)
        hand.fingers = {"THUMB": Hand.Finger(),
                        "INDEX_FINGER": Hand.Finger(),
                        "MIDDLE_FINGER": Hand.Finger(),
                        "RING_FINGER": Hand.Finger(),
                        "PINKY": Hand.Finger()}
        hand.fingers["INDEX_FINGER"].tip = index_tip

        # Act
        actual: Point = hand.get_index_tip()

        # Assert
        assert actual == index_tip

    # TODO: Write test case
    def test_get_mask_points(self):
        pass

    # TODO: Write test case
    def test_update_finger(self):
        pass
