import math


class GestureDetector:

    def __init__(self):
        self.was_pinching = False

    def detect_pinch(self, hand):

        thumb_tip = hand[4]
        index_tip = hand[8]

        distance = math.sqrt(
            (thumb_tip.x - index_tip.x) ** 2
            + (thumb_tip.y - index_tip.y) ** 2
        )

        pinching = distance < 0.05

        pinch_started = pinching and not self.was_pinching

        self.was_pinching = pinching

        return pinch_started

    def detect_index_direction(self, hand):

        index_base = hand[5]
        index_tip = hand[8]

        dy = index_tip.y - index_base.y

        threshold = 0.05

        if dy < -threshold:
            return "up"

        if dy > threshold:
            return "down"

        return None