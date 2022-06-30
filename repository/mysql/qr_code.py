import model.mysql as model
from mysql import MySQL


class QRCode:
    _mysql: MySQL

    def __init__(self, mysql: MySQL):
        self._mysql = mysql

    def list(self):
        qrCodes = self._mysql.get_db().query(model.QRCode).all()
        print(qrCodes)
