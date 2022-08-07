from repository.mysql.qr_code import QRCode as QRCodeRepo
import model.mysql as model

Features = list[float]

class QRCode:
    _repo: QRCodeRepo

    def __init__(self, repo: QRCodeRepo):
        self._repo = repo

    def list(self):
        self._repo.list()

    def add(self, features: Features):
        # TODO: s3upload
        s3_uri = ''
        qr_code = self._repo.add(s3_uri, features)
        return qr_code

    def get_best_candidate(self, features: Features) -> int | None:
        qr_code_count_dict: dict[int] = {}
        for feature in features:
            print(feature)
            # TODO: widthの範囲を考える
            qr_code_counts = self._repo.list_qr_code_count_by_feature_with_width(feature, 0)
            for qr_code_count in qr_code_counts:
                if qr_code_count.id in qr_code_count_dict:
                    qr_code_count_dict[qr_code_count.id] += qr_code_count.count
                else:
                    qr_code_count_dict[qr_code_count.id] = qr_code_count.count
        if len(qr_code_count_dict.keys()) == 0:
            return None
        max_item = max(qr_code_count_dict.items(), key=lambda item: item[1])
        return self._repo.get(max_item[0])



