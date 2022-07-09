import math

from llah.keypoint import Keypoint
from scipy.spatial import KDTree
import copy
import numpy as np

class DescriptorExtractor:
    _m: int

    def __init__(self, m: int):
        self._m = m

    @classmethod
    def triangle_perimeter(cls, p1: Keypoint, p2: Keypoint, p3: Keypoint):
        return p1.distance_from(p2) + p2.distance_from(p3) + p3.distance_from(p1)

    def sample_keypoint(self, keypoints: list[Keypoint], num: int):
        if len(keypoints) < num:
            return keypoints

        sampledKeypoints: list[Keypoint] = []
        # add: c++のコードで重複点削除に対応していなかったので対応
        remainingKeypoints = copy.copy(keypoints)
        additionalSampledKeypoints: list[Keypoint] = []

        coordinates = list(map(lambda item: [item.x, item.y], keypoints))
        kdTree = KDTree(coordinates)
        for i, keypoint in enumerate(keypoints):
            distances, indexes = kdTree.query([keypoint.x, keypoint.y], self._m + 1)
            isMinimumKeypoint = all(map(lambda index: keypoint.size < keypoints[index].size, indexes[1:]))
            if isMinimumKeypoint:
                sampledKeypoints.append(keypoint)
                del remainingKeypoints[i - len(sampledKeypoints)]
                # add: c++のコードでは引数のnumを超える可能性があった
                if len(sampledKeypoints) == num:
                    return sampledKeypoints

        lackNum = num - len(sampledKeypoints)
        addNumAroundKeypoint = math.floor(lackNum / len(sampledKeypoints))
        lackAddNum = lackNum % len(sampledKeypoints)
        interval = 0 if lackAddNum == 0 else math.floor(len(sampledKeypoints) / lackAddNum)

        for i, keypoint in enumerate(sampledKeypoints):
            remainingCoordinates = list(map(lambda item: [item.x, item.y], remainingKeypoints))
            # TODO: 計算の重さを測る
            remainingKDTree = KDTree(remainingCoordinates)
            addNum = addNumAroundKeypoint
            if interval != 0 and (i+1) % interval == 0 and lackAddNum > 0:
                addNum += 1
                lackAddNum -= 1
            if addNum == 0:
                continue

            _, indexes = remainingKDTree.query([keypoint.x, keypoint.y], addNum)
            if type(indexes) is np.ndarray:
                for j, index in enumerate(indexes):
                    additionalSampledKeypoints.append(remainingKeypoints[index - j])
                    del remainingKeypoints[index - j]
            else:
                index = indexes
                additionalSampledKeypoints.append(remainingKeypoints[index])
                del remainingKeypoints[index]

        sampledKeypoints.extend(additionalSampledKeypoints)
        return sampledKeypoints


