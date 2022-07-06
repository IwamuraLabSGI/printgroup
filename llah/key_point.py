import math


class KeyPoint:
    pass


class KeyPoint:
    def __int__(self, x: float, y: float, size: float):
        self.x = x
        self.y = y
        self.size = size

    def distance_from(self, key_point: KeyPoint):
        return math.sqrt((self.x - key_point.x) ^ 2 + (self.y - key_point.y) ^ 2)
