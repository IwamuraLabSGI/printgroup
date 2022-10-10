import itertools
import math

from llah.keypoint import Keypoint
import copy
import numpy as np
from dataclasses import dataclass


@dataclass
class TriangleRateAttribute:
    start_index: int
    perimeter_rate: float
    area_rate: float
    arg_rate: float


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

    @classmethod
    def triangle_arg(cls, p1: Keypoint, p2: Keypoint, p3: Keypoint):
        return math.atan2(p2.y - p1.y, p2.x - p1.x) - math.atan2(p3.y - p1.y, p3.x - p1.x)

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

    def extract(self, keypoints: list[Keypoint]) -> Descriptors:
        if len(keypoints) < self._neighbor_total + self._additional_neighbor_total:
            raise ValueError('特徴点の数が足りません。')

        kd_tree = Keypoint.get_kd_tree(keypoints)
        descriptors: Descriptors = []
        for i, keypoint in enumerate(keypoints):
            limit = self._neighbor_total + self._additional_neighbor_total + 1
            _, indexes = kd_tree.query([keypoint.x, keypoint.y], limit)
            # 近傍点から特徴量を全パターン計算
            neighbor_indexes = indexes[1:]

            descriptor = Descriptor(keypoint, [])
            for combination in itertools.combinations(neighbor_indexes, self._neighbor_total):
                neighbors = list(map(lambda index: keypoints[index], combination))
                # 時計回りに近傍点を3点ずつって特徴量を計算
                neighbors.sort(key=lambda item: np.arctan2(item.x - keypoint.x, item.y - keypoint.y))
                start_indexes = range(0, len(neighbors), 1)

                attributes: TriangleRateAttributes = []
                for start_index in start_indexes:
                    targets: list[Keypoint] = []
                    end_index = start_index + 3
                    if end_index >= len(neighbors):
                        targets.extend(neighbors[start_index:])
                        targets.extend(neighbors[0:end_index - len(neighbors)])
                    else:
                        targets.extend(neighbors[start_index:end_index])

                    perimeter_rate: float = 0
                    perimeter = DescriptorExtractor.triangle_perimeter(keypoint, targets[0], targets[1])
                    next_perimeter = DescriptorExtractor.triangle_perimeter(keypoint, targets[1], targets[2])
                    # TODO: 分母が0になるような場合を確認
                    if next_perimeter != 0:
                        perimeter_rate = perimeter / next_perimeter

                    area_rate: float = 0
                    area = DescriptorExtractor.triangle_area(keypoint, targets[0], targets[1])
                    next_area = DescriptorExtractor.triangle_area(keypoint, targets[1], targets[2])
                    if next_area != 0:
                        area_rate = area / next_area

                    arg_rate: float = 0
                    arg = DescriptorExtractor.triangle_arg(keypoint, targets[0], targets[1])
                    next_arg = DescriptorExtractor.triangle_arg(keypoint, targets[1], targets[2])
                    if next_arg != 0:
                        arg_rate = arg / next_arg

                    attributes.append(TriangleRateAttribute(
                        start_index=start_index,
                        perimeter_rate=perimeter_rate,
                        area_rate=area_rate,
                        arg_rate=arg_rate
                    ))
                descriptor.multi_pattern_attributes.append(attributes)
                # TODO: 必要なら面積比の特徴量も
            descriptors.append(descriptor)
        return descriptors

    @classmethod
    def risannka(cls, rate: float) -> int:
        if rate < 0.40:
            return 0
        elif rate < 0.66:
            return 1
        elif rate < 0.80:
            return 2
        elif rate < 1.00:
            return 3
        elif rate < 1.20:
            return 4
        elif rate < 1.40:
            return 5
        elif rate < 1.60:
            return 6
        elif rate < 1.80:
            return 7
        elif rate < 1.90:
            return 8
        else:
            return 9

    def old_extract(self, keypoints: list[Keypoint]):
        descriptors: list[float] = []
        if len(keypoints) < self._neighbor_total + self._additional_neighbor_total:
            try:
                raise ValueError('特徴点の数が少ないです。')
            except ValueError as e:
                return descriptors

        kd_tree = Keypoint.get_kd_tree(keypoints)
        for i, keypoint in enumerate(keypoints):
            limit = self._neighbor_total + self._additional_neighbor_total + 1
            _, indexes = kd_tree.query([keypoint.x, keypoint.y], limit)
            # 近傍点から特徴量を全パターン計算
            neighbor_indexes = indexes[1:]
            keypoint_attributes: list[float] = []
            for combination in itertools.combinations(neighbor_indexes, self._neighbor_total):
                attribute = 0
                c = list(range(0, self._neighbor_total - 1))
                a = list(itertools.combinations(c, 3))
                b = list(itertools.combinations(c, 4))
                neighbors = list(map(lambda index: keypoints[index], combination))
                # 時計回りに近傍点を3点ずつって特徴量を計算
                neighbors.sort(key=lambda item: np.arctan2(item.x - keypoint.x, item.y - keypoint.y))
                for j in range(len(a)):
                    triangle_perimeter_1 = DescriptorExtractor \
                        .triangle_perimeter(keypoint, neighbors[a[j][0]], neighbors[a[j][1]])
                    triangle_perimeter_2 = DescriptorExtractor \
                        .triangle_perimeter(keypoint, neighbors[a[j][1]], neighbors[a[j][2]])
                    if triangle_perimeter_1 != 0 and triangle_perimeter_2 != 0:
                        triangle_perimeter_rate = triangle_perimeter_1 / triangle_perimeter_2
                        triangle_perimeter_rate = DescriptorExtractor.risannka(triangle_perimeter_rate)
                        attribute = attribute + triangle_perimeter_rate * (10 ** j)
                for j in range(len(b)):
                    triangle_perimeter_1 = DescriptorExtractor \
                        .triangle_perimeter(neighbors[b[j][0]], neighbors[b[j][1]], neighbors[b[j][2]])
                    triangle_perimeter_2 = DescriptorExtractor \
                        .triangle_perimeter(neighbors[b[j][0]], neighbors[b[j][2]], neighbors[b[j][3]])
                    if triangle_perimeter_1 != 0 and triangle_perimeter_2 != 0:
                        triangle_perimeter_rate = triangle_perimeter_1 / triangle_perimeter_2
                        triangle_perimeter_rate = DescriptorExtractor.risannka(triangle_perimeter_rate)
                        attribute = attribute + triangle_perimeter_rate * (10 ** (j + len(a) + 1))
                keypoint_attributes.append(attribute)
            descriptors.extend(keypoint_attributes)
        return descriptors
