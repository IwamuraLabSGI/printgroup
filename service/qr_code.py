import math
import uuid

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
        sampled_features: model.QRCodeFeatures = []
        sample_span = math.floor(len(features) / 100)
        for i in range(100):
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
    def get_mode_id(cls, ids: model.Ids) -> int:
        return max(set(ids), key=ids.count)

    def get_best_candidate_v2(
            self,
            cyan_features: model.QRCodeFeatures,
            magenta_features: model.QRCodeFeatures,
            yellow_features: model.QRCodeFeatures
    ) -> model.QRCode | None:
        cyan_features = QRCode.__sample_features(cyan_features)

        cyan_qr_code_ids = self._repo.get_qr_code_ids_by_color_features(
            color=model.QRCodeFeatureColor.cyan,
            features=cyan_features
        )
        cyan_mode_id = QRCode.get_mode_id(cyan_qr_code_ids)

        magenta_features = QRCode.__sample_features(magenta_features)
        magenta_qr_code_ids = self._repo.get_qr_code_ids_by_color_features(
            color=model.QRCodeFeatureColor.magenta,
            features=magenta_features
        )
        magenta_mode_id = QRCode.get_mode_id(magenta_qr_code_ids)

        yellow_features = QRCode.__sample_features(yellow_features)
        yellow_qr_code_ids = self._repo.get_qr_code_ids_by_color_features(
            color=model.QRCodeFeatureColor.yellow,
            features=yellow_features
        )
        yellow_mode_id = QRCode.get_mode_id(yellow_qr_code_ids)

        if cyan_mode_id == magenta_mode_id == yellow_mode_id:
            return self._repo.get(cyan_mode_id)
        else:
            return None
