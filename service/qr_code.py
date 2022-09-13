import collections
import math
import uuid

import numpy as np

import llah
from domain import CmykKeypointExtractor, FeatureCalculator
from repository.mysql.qr_code import QRCode as QRCodeRepo
from model import mysql as model


class QRCode:
    _repo: QRCodeRepo

    def __init__(self, repo: QRCodeRepo):
        self._repo = repo

    def list(self):
        self._repo.list()

    def add(self, file_name: str, features: model.QRCodeFeatures) -> model.QRCode:
        # TODO: s3upload
        s3_uri = uuid.uuid4()
        qr_code = self._repo.add(
            s3_uri=s3_uri,
            file_name=file_name,
            features=features
        )
        return qr_code

    @classmethod
    def __sample_features(cls, features: model.QRCodeFeatures) -> model.QRCodeFeatures:
        sample_total = 500
        sampled_features: model.QRCodeFeatures = []
        sample_span = math.floor(len(features) / sample_total)
        for i in range(sample_total):
            sampled_features.append(features[i*sample_span])
        return sampled_features

    def get_best_candidate(self, features: model.QRCodeFeatures) -> model.QRCode | None:
        features = QRCode.__sample_features(features)
        qr_code_count_dict: dict[int, int] = {}
        for feature in features:
            qr_code_ids = self._repo.list_qr_code_ids_by_feature(feature)
            for qr_code_id in qr_code_ids:
                if qr_code_id in qr_code_count_dict:
                    qr_code_count_dict[qr_code_id] += 1
                else:
                    qr_code_count_dict[qr_code_id] = 1
        print(qr_code_count_dict)
        if len(qr_code_count_dict.keys()) == 0:
            return None
        max_item = max(qr_code_count_dict.items(), key=lambda item: item[1])
        return self._repo.get(max_item[0])

    @classmethod
    def get_mode_id(cls, ids: model.Ids) -> int | None:
        if len(ids) == 0:
            return None
        return max(set(ids), key=ids.count)

    def find_qr_code(
        self,
        img: np.ndarray,
    ) -> model.QRCode | None:
        cmy_keypoints = CmykKeypointExtractor.extract(img)

        descriptor_extractor = llah.DescriptorExtractor(6, 2)

        cyan_descriptors = descriptor_extractor.extract(cmy_keypoints.get('cyan'))
        magenta_descriptors = descriptor_extractor.extract(cmy_keypoints.get('magenta'))
        yellow_descriptors = descriptor_extractor.extract(cmy_keypoints.get('yellow'))

        cyan_features = list(map(lambda item: model.QRCodeFeature(
            feature=item,
            color=model.QRCodeFeatureColor.cyan
        ), FeatureCalculator.calc(cyan_descriptors)))

        magenta_features = list(map(lambda item: model.QRCodeFeature(
            feature=item,
            color=model.QRCodeFeatureColor.magenta
        ), FeatureCalculator.calc(magenta_descriptors)))

        yellow_features = list(map(lambda item: model.QRCodeFeature(
            feature=item,
            color=model.QRCodeFeatureColor.yellow
        ), FeatureCalculator.calc(yellow_descriptors)))

        features: model.QRCodeFeatures = []
        features.extend(QRCode.__sample_features(cyan_features))
        features.extend(QRCode.__sample_features(magenta_features))
        features.extend(QRCode.__sample_features(yellow_features))

        features = self._repo.list_features(features)
        qr_code_ids = list(map(lambda feature: feature.qr_code_id, features))

        # counter = collections.Counter(qr_code_ids)
        # print(counter)

        if len(qr_code_ids) == 0:
            return None
        return self._repo.get(QRCode.get_mode_id(qr_code_ids))
