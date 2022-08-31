import uuid

from repository.mysql.qr_code import QRCode as QRCodeRepo
import model.mysql as model

Features = list[float]


class QRCode:
    _repo: QRCodeRepo

    def __init__(self, repo: QRCodeRepo):
        self._repo = repo

    def list(self):
        self._repo.list()

    def add(self, file_name: str, features: Features):
        # TODO: s3upload
        s3_uri = uuid.uuid4()
        qr_code = self._repo.add(
            s3_uri=s3_uri,
            file_name=file_name,
            features=features
        )
        return qr_code

    def get_best_candidate(self, features: Features) -> int | None:
        qr_code_count_dict: dict[int, int] = {}
        for feature in features:
            hash = feature
            # TODO: widthの範囲を考える
            qr_code_ids = self._repo.list_qr_code_ids_by_hash_with_width(hash, 0)
            for qr_code_id in qr_code_ids:
                if qr_code_id in qr_code_count_dict:
                    qr_code_count_dict[qr_code_id] += 1
                else:
                    qr_code_count_dict[qr_code_id] = 1
        if len(qr_code_count_dict.keys()) == 0:
            return None
        max_item = max(qr_code_count_dict.items(), key=lambda item: item[1])
        return self._repo.get(max_item[0])
