from repository.mysql.qr_code import QRCode as QRCodeRepo


class QRCode:
    _repo: QRCodeRepo

    def __init__(self, repo: QRCodeRepo):
        self._repo = repo

    def list(self):
        self._repo.list()
