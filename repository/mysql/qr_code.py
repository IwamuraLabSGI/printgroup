import model.mysql as model
from mysql import MySQL
from sqlalchemy import func

Features = list[float]
QRCodeCounts = list[model.QRCodeCount]
QRCodes = list[model.QRCode]


class QRCode:
    _mysql: MySQL

    def __init__(self, mysql: MySQL):
        self._mysql = mysql

    def get(self, id: int) -> model.QRCode:
        qr_code = self._mysql.get_db().query(model.QRCode).\
            filter(model.QRCode.id == id).\
            first()
        return qr_code

    def list(self) -> QRCodes:
        qr_codes = self._mysql.get_db().query(model.QRCode).all()
        return qr_codes

    def list_qr_code_count_by_feature_with_width(self, feature: float, width: float) -> QRCodeCounts:
        db = self._mysql.get_db()
        res = db.query(
                model.QRCodeFeature.qr_code_id,
                func.count(model.QRCodeFeature.qr_code_id)
            ).\
            filter(model.QRCodeFeature.feature.between(feature-width/2, feature+width/2)). \
            group_by(model.QRCodeFeature.qr_code_id).\
            all()
        qr_code_counts = list(map(lambda item: model.QRCodeCount(id=item[0], count=item[1]), res))
        return qr_code_counts

    def list_qr_code_count_by_feature(self, feature: float) -> QRCodeCounts:
        db = self._mysql.get_db()
        res = db.query(
                model.QRCodeFeature.qr_code_id,
                func.count(model.QRCodeFeature.qr_code_id)
            ).\
            where(model.QRCodeFeature.feature == feature).\
            group_by(model.QRCodeFeature.qr_code_id).\
            all()
        qr_code_counts = list(map(lambda item: model.QRCodeCount(id=item[0], count=item[1]), res))
        return qr_code_counts

    def add(self, s3_uri: str, features: Features) -> model.QRCode:
        db = self._mysql.get_db()

        # TODO: transaction
        qr_code = model.QRCode(
            s3_uri=s3_uri
        )
        db.add(qr_code)
        db.flush()

        qr_code_features = list(map(lambda feature: model.QRCodeFeature(
            qr_code_id=qr_code.id,
            feature=feature
        ), features))
        db.bulk_save_objects(qr_code_features)
        db.commit()

        return qr_code
