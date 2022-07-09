from keypoint import KeyPoint


class Node:
    def __init__(self, key_point: KeyPoint):
        self.key_point = key_point
        self.left = None
        self.right = None

    def has_left_node(self):
        return self.left is not None

    def has_right_node(self):
        return self.right is not None
