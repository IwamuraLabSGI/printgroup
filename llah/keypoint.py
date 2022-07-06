import math


class Keypoint:
    pass


class Keypoint:
    x: float
    y: float
    size: float

    def __init__(self, x: float, y: float, size: float):
        self.x = x
        self.y = y
        self.size = size

    def distance_from(self, keypoint: Keypoint):
        return math.sqrt((self.x - keypoint.x) ^ 2 + (self.y - keypoint.y) ^ 2)
