from repository.mysql.qr_code import QRCode as QRCodeRepo

Features = list[float]

class QRCode:
    _repo: QRCodeRepo

    def __init__(self, repo: QRCodeRepo):
        self._repo = repo

    def list(self):
        self._repo.list()

    def add(self, features: Features):
        # # TODO: s3upload
        s3_uri = ''
        qr_code = self._repo.add(s3_uri, features)
        return qr_code


