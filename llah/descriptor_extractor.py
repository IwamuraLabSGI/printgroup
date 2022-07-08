import itertools
import math

from llah.keypoint import Keypoint
from scipy.spatial import KDTree
import copy
import numpy as np


class DescriptorExtractor:
    # 特徴量の計算に使用する近傍点の数
    # edit: c++では_mという名前
    # _m = _neighbor_total
    _neighbor_total: int

    # 特徴量の候補を増やすために追加で使用する近傍てんの数
    # edit: c++では候補として使用する特徴点の総数を_nとしていたが、
    # わかりにくいので、候補の数を設定することにしました
    # _n = _neighbor_total + _neighbor_candidate_total
    _neighbor_candidate_total: int

    def __init__(self, neighbor_total: int, neighbor_candidate_total: int):
        self._neighbor_total = neighbor_total
        self._neighbor_candidate_total = neighbor_candidate_total

    @classmethod
    def triangle_perimeter(cls, p1: Keypoint, p2: Keypoint, p3: Keypoint):
        return p1.distance_from(p2) + p2.distance_from(p3) + p3.distance_from(p1)

    # QRコードは英文書と異なり、特徴点領域の面積はほぼ均等で、特徴点の分散は色の濃度によるのでサンプリング手法は変えた方が良さそう
    def __sample_keypoint(self, keypoints: list[Keypoint], num: int):
        if len(keypoints) < num:
            return keypoints

        sampledKeypoints: list[Keypoint] = []
        # add: c++のコードで重複点削除に対応していなかったので対応
        remainingKeypoints = copy.copy(keypoints)
        additionalSampledKeypoints: list[Keypoint] = []

        kdTree = Keypoint.get_kd_tree(keypoints)
        for i, keypoint in enumerate(keypoints):
            _, indexes = kdTree.query([keypoint.x, keypoint.y], self._neighbor_total + 1)
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
            # TODO: 計算の重さを測る
            remainingKDTree = Keypoint.get_kd_tree(remainingKeypoints)
            addNum = addNumAroundKeypoint
            if interval != 0 and (i + 1) % interval == 0 and lackAddNum > 0:
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

    def extract(self, keypoints: list[Keypoint]):
        if len(keypoints) < self._neighbor_total + self._neighbor_candidate_total:
            raise ValueError('特徴点の数が足りません。')

        # TODO: sampling処理追加
        kdTree = Keypoint.get_kd_tree(keypoints)
        descriptors: list[list[float]] = []
        for i, keypoint in enumerate(keypoints):
            limit = self._neighbor_total + self._neighbor_candidate_total + 1
            _, indexes = kdTree.query([keypoint.x, keypoint.y], limit)
            # 近傍点から特徴量を全パターン計算
            neighborIndexes = indexes[1:]
            for combination in itertools.combinations(neighborIndexes, self._neighbor_total):
                neighbors = list(map(lambda index: keypoints[index], combination))
                # 時計回りに近傍点を3点ずつって特徴量を計算
                neighbors.sort(key=lambda item: np.arctan2(item.x - keypoint.x, item.y - keypoint.y))
                target_total = math.floor(len(neighbors) / 2)
                for target_num in range(target_total-1):
                    target = neighbors[target_num*3:target_num*3+3]
                    # add: c++ではrateが1以下になるように逆数をとっていたが特に意味もなさそうなので削除
                    triangle_perimeter_rate = \
                        DescriptorExtractor.triangle_perimeter(keypoint, target[0], target[1]) \
                        / DescriptorExtractor.triangle_perimeter(keypoint, target[1], target[2])
                    # TODO:
                    print(triangle_perimeter_rate)
