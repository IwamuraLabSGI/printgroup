from keypoint import KeyPoint
from node import Node

class BinaryTree:
    root: Node = None

    def __init__(self):
        self.root = None

    def insert(self, point: KeyPoint):
        depth = 0
        root = self.root
        if root is None:
            self.root = Node(root)
            return
        while True:
            ++depth
            isEven = bool(depth & 1)
            root_key_point = root.key_point