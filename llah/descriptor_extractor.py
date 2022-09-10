import itertools
import math

from llah.keypoint import Keypoint
from scipy.spatial import KDTree
import copy
import numpy as np
from dataclasses import dataclass



@dataclass
class TriangleRateAttribute:
    start_index: int
    perimeter_rate: float
    area_rate: float


TriangleRateAttributes = list[TriangleRateAttribute]


@dataclass
class Descriptor:
    keypoint: Keypoint
    multi_pattern_attributes: list[TriangleRateAttributes]


Descriptors = list[Descriptor]


class DescriptorExtractor:
    # 特徴量の計算に使用する近傍点の数
    # edit: c++では_mという名前
    # _m = _neighbor_total
    _neighbor_total: int

    # 特徴量の候補を増やすために追加で使用する近傍てんの数
    # edit: c++では候補として使用する特徴点の総数を_nとしていたが、
    # わかりにくいので、候補の数を設定することにしました
    # _n = _neighbor_total + _additional_neighbor_total
    _additional_neighbor_total: int

    def __init__(self, neighbor_total: int, additional_neighbor_total: int):
        self._neighbor_total = neighbor_total
        self._additional_neighbor_total = additional_neighbor_total

    @classmethod
    def triangle_perimeter(cls, p1: Keypoint, p2: Keypoint, p3: Keypoint):
        return p1.distance_from(p2) + p2.distance_from(p3) + p3.distance_from(p1)

    @classmethod
    def triangle_area(cls, p1: Keypoint, p2: Keypoint, p3: Keypoint):
        return abs((p1.x - p3.x) * (p2.y - p1.y) - (p1.x - p2.x) * (p3.y - p1.y)) / 2

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
            # TODO: 距離の昇順で返ってきているか確認
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
        if len(keypoints) < self._neighbor_total + self._additional_neighbor_total:
            raise ValueError('特徴点の数が足りません。')

        # TODO: sampling処理追加
        kd_tree = Keypoint.get_kd_tree(keypoints)
        descriptors: Descriptors = []
        for i, keypoint in enumerate(keypoints):
            limit = self._neighbor_total + self._additional_neighbor_total + 1
            _, indexes = kd_tree.query([keypoint.x, keypoint.y], limit)
            # 近傍点から特徴量を全パターン計算
            neighbor_indexes = indexes[1:]

            descriptor = Descriptor(keypoint, [])
            for combination in itertools.combinations(neighbor_indexes, self._neighbor_total):
                # TODO: get_neighbors切り出し
                neighbors = list(map(lambda index: keypoints[index], combination))
                # 時計回りに近傍点を3点ずつって特徴量を計算
                neighbors.sort(key=lambda item: np.arctan2(item.x - keypoint.x, item.y - keypoint.y))
                target_total = math.floor(len(neighbors) / 2)

                attributes: TriangleRateAttributes = []
                for target_num in range(target_total):
                    target: list[Keypoint] = []
                    start_index = target_num * 2
                    end_index = start_index + 3
                    if end_index > len(neighbors):
                        target.extend(neighbors[start_index:])
                        target.extend(neighbors[0:1])
                    else:
                        target.extend(neighbors[start_index:end_index])

                    perimeter_rate: float = 0
                    # add: c++ではrateが1以下になるように逆数をとっていたが特に意味もなさそうなので削除
                    perimeter = DescriptorExtractor.triangle_perimeter(keypoint, target[0], target[1])
                    next_perimeter = DescriptorExtractor.triangle_perimeter(keypoint, target[1], target[2])
                    # TODO: 分母が0になるような場合を確認
                    if next_perimeter != 0:
                        perimeter_rate = perimeter / next_perimeter

                    area_rate: float = 0
                    area = DescriptorExtractor.triangle_area(keypoint, target[0], target[1])
                    next_area = DescriptorExtractor.triangle_area(keypoint, target[1], target[2])
                    if next_area != 0:
                        area_rate = area / next_area

                    attributes.append(TriangleRateAttribute(
                        start_index=start_index,
                        perimeter_rate=perimeter_rate,
                        area_rate=area_rate
                    ))
                descriptor.multi_pattern_attributes.append(attributes)
                # TODO: 必要なら面積比の特徴量も
            descriptors.append(descriptor)
        return descriptors

    def OLDextract(self, keypoints: list[Keypoint]):
        descriptors: list[float] = []
        if len(keypoints) < self._neighbor_total + self._additional_neighbor_total:
            try:
                raise ValueError('特徴点の数が少ないです。')
            except ValueError as e:
                return descriptors
        j = 0
        kk = 0
        # TODO: sampling処理追加
        kdTree = Keypoint.get_kd_tree(keypoints)

        for i, keypoint in enumerate(keypoints):
            limit = self._neighbor_total + self._additional_neighbor_total + 1
            _, indexes = kdTree.query([keypoint.x, keypoint.y], limit)
            # 近傍点から特徴量を全パターン計算
            neighborIndexes = indexes[1:]
            keypoint_attributes: list[float] = []
            for combination in itertools.combinations(neighborIndexes, self._neighbor_total):
                d = 0
                e = 0
                c = list(range(0, self._neighbor_total - 1))
                a = itertools.combinations(c, 3)
                a = list(a)
                b = itertools.combinations(c, 4)
                b = list(b)
                # TODO: get_neighbors切り出し
                neighbors = list(map(lambda index: keypoints[index], combination))
                # 時計回りに近傍点を3点ずつって特徴量を計算
                neighbors.sort(key=lambda item: np.arctan2(item.x - keypoint.x, item.y - keypoint.y))
                perimeter_rate_attributes: list[float] = []
                for i in range(len(a)):
                    if (DescriptorExtractor.triangle_perimeter(keypoint, neighbors[a[i][1]], neighbors[
                        a[i][2]]) != 0 and DescriptorExtractor.triangle_perimeter(keypoint, neighbors[a[i][0]],
                                                                                  neighbors[a[i][1]]) != 0):
                        triangle_perimeter_rate = \
                            DescriptorExtractor.triangle_perimeter(keypoint, neighbors[a[i][0]], neighbors[a[i][1]]) \
                            / DescriptorExtractor.triangle_perimeter(keypoint, neighbors[a[i][1]], neighbors[a[i][2]])
                        triangle_perimeter_rate = DescriptorExtractor.risannka(triangle_perimeter_rate)
                        e = e + triangle_perimeter_rate * (10 ** d)
                        d = d + 1
                    # TODO: 離散化
                for i in range(len(b)):
                    if (DescriptorExtractor.triangle_perimeter(neighbors[b[i][0]], neighbors[b[i][1]], neighbors[
                        b[i][2]]) != 0 and DescriptorExtractor.triangle_perimeter(neighbors[b[i][0]],
                                                                                  neighbors[b[i][2]],
                                                                                  neighbors[b[i][3]])):
                        triangle_perimeter_rate = \
                            DescriptorExtractor.triangle_perimeter(neighbors[b[i][0]], neighbors[b[i][1]],
                                                                   neighbors[b[i][2]]) \
                            / DescriptorExtractor.triangle_perimeter(neighbors[b[i][0]], neighbors[b[i][2]],
                                                                     neighbors[b[i][3]])
                        triangle_perimeter_rate = DescriptorExtractor.risannka(triangle_perimeter_rate)
                        e = e + triangle_perimeter_rate * (10 ** d)
                        d = d + 1
                # TODO: 離散化
                perimeter_rate_attributes.append(e)
                keypoint_attributes.append(e)
                j = j + 1
                # TODO: 必要なら面積比の特徴量も
            descriptors.extend(keypoint_attributes)
        print("総特徴量数：", len(descriptors))
        return descriptors
