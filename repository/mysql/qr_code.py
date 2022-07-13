import model.mysql as model
from mysql import MySQL

Features = list[float]

class QRCode:
    _mysql: MySQL

    def __init__(self, mysql: MySQL):
        self._mysql = mysql

    def list(self):
        qrCodes = self._mysql.get_db().query(model.QRCode).all()
        print(qrCodes)

    def add(self, s3_uri: str, features: Features):
        db = self._mysql.get_db()

        # TODO: transaction
        qr_code = model.QRCode(
            s3_uri=s3_uri
        )
        db.add(qr_code)
        db.commit()

        qr_code_features = list(map(lambda feature: model.QRCodeFeature(
            qr_code_id=qr_code.id,
            feature=feature
        ), features))
        db.bulk_save_objects(qr_code_features)
        db.commit()

        return qr_code
