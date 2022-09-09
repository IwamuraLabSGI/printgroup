import math
from scipy.spatial import KDTree


class Keypoint:
    pass


class Keypoint:
    x: float
    y: float
    size: float

    @classmethod
    def get_kd_tree(cls, keypoints: list[Keypoint]):
        coordinates = list(map(lambda item: [item.x, item.y], keypoints))
        return KDTree(coordinates)

    def __init__(self, x: float, y: float, size: float):
        self.x = x
        self.y = y
        self.size = size

    def distance_from(self, keypoint: Keypoint):
        return math.sqrt((self.x - keypoint.x) ** 2 + (self.y - keypoint.y) ** 2)


Keypoints = list[Keypoint]