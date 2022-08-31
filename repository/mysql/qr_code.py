import model.mysql as model
from schema.mysql import MySQL
from sqlalchemy import func

Features = list[float]
Ids = list[int]
QRCodeCounts = list[model.QRCodeCount]
QRCodes = list[model.QRCode]
QRCodeFeatures = list[model.QRCodeFeature]


class QRCode:
    _mysql: MySQL

    def __init__(self, mysql: MySQL):
        self._mysql = mysql

    def get(self, id: int) -> model.QRCode:
        qr_code = self._mysql.get_session().query(model.QRCode).\
            filter(model.QRCode.id == id).\
            first()
        return qr_code

    def update(self, item: model.QRCode) -> model.QRCode:
        session = self._mysql.get_session()
        session.merge(item)
        session.commit()
        return item

    def bulk_update(self, items: QRCodes):
        session = self._mysql.get_session()
        session.bulk_update_mappings(items)
        session.commit()

    def list(self) -> QRCodes:
        qr_codes = self._mysql.get_session().query(model.QRCode).all()
        return qr_codes

    def list_qr_code_count_by_feature_with_width(self, feature: float, width: float) -> QRCodeCounts:
        session = self._mysql.get_session()
        res = session.query(
                model.QRCodeFeature.qr_code_id,
                func.count(model.QRCodeFeature.qr_code_id)
            ).\
            filter(model.QRCodeFeature.feature.between(feature-width/2, feature+width/2)). \
            group_by(model.QRCodeFeature.qr_code_id).\
            all()
        qr_code_counts = list(map(lambda item: model.QRCodeCount(id=item[0], count=item[1]), res))
        return qr_code_counts

    def list_qr_code_ids_by_hash_with_width(self, hash: float, width: float) -> Ids:
        session = self._mysql.get_session()
        res = session.\
            query(model.QRCodeFeatureHashCache.qr_code_ids).\
            filter(model.QRCodeFeatureHashCache.hash.between(hash - width / 2, hash + width / 2)).\
            first()
        return res[0]

    def list_qr_code_count_by_feature(self, feature: float) -> QRCodeCounts:
        session = self._mysql.get_session()
        res = session.query(
                model.QRCodeFeature.qr_code_id,
                func.count(model.QRCodeFeature.qr_code_id)
            ).\
            where(model.QRCodeFeature.feature == feature).\
            group_by(model.QRCodeFeature.qr_code_id).\
            all()
        qr_code_counts = list(map(lambda item: model.QRCodeCount(id=item[0], count=item[1]), res))
        return qr_code_counts

    def add(self, s3_uri: str, file_name: str, features: Features) -> model.QRCode:
        session = self._mysql.get_session()

        # TODO: transaction
        qr_code = model.QRCode(
            s3_uri=s3_uri,
            file_name=file_name
        )
        session.add(qr_code)
        session.flush()

        qr_code_features = list(map(lambda feature: model.QRCodeFeature(
            qr_code_id=qr_code.id,
            feature=feature
        ), features))
        session.bulk_save_objects(qr_code_features)
        session.commit()

        return qr_code

    def delete(self, qr_code_id):
        session = self._mysql.get_session()
        session.query(model.QRCode).filter(model.QRCode.id == qr_code_id).delete()
        session.query(model.QRCodeFeature).filter(model.QRCodeFeature.qr_code_id == qr_code_id).delete()
        session.commit()

    def list_by_is_feature_hash_cache_created(self, is_created: bool) -> QRCodes:
        session = self._mysql.get_session()
        qr_codes = session.\
            query(model.QRCode).\
            where(model.QRCode.is_feature_hash_cache_created == is_created).\
            all()
        return qr_codes

    def update_qr_code_features(self, qr_code_id: int, features: Features):
        session = self._mysql.get_session()
        qr_code_features = list(map(lambda feature: model.QRCodeFeature(
            qr_code_id=qr_code_id,
            feature=feature
        ), features))
        session.bulk_save_objects(qr_code_features)
        session.commit()

    def list_by_feature_hash_cache_created(self, feature_hash_cache_created: bool) -> QRCodes:
        session = self._mysql.get_session()
        qr_codes = session.\
            query(model.QRCode).\
            where(model.QRCode.feature_hash_cache_created == feature_hash_cache_created).\
            all()
        return qr_codes

    def list_qr_code_features_by_qr_code_is(self, qr_code_id) -> QRCodeFeatures:
        session = self._mysql.get_session()
        features = session.\
            query(model.QRCodeFeature).\
            where(model.QRCodeFeature.qr_code_id == qr_code_id).\
            all()
        return features


