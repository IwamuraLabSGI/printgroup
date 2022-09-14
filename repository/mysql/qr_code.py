from sqlalchemy import or_, and_

import model.mysql as model
from schema.mysql import MySQL

QRCodeCounts = list[model.QRCodeCount]


class QRCode:
    _mysql: MySQL

    def __init__(self, mysql: MySQL):
        self._mysql = mysql

    def get(self, qr_code_id: int) -> model.QRCode | None:
        qr_code = self._mysql.get_session().query(model.QRCode).\
            filter(model.QRCode.id == qr_code_id).\
            first()
        return qr_code

    def update(self, item: model.QRCode) -> model.QRCode:
        session = self._mysql.get_session()
        session.merge(item)
        session.commit()
        return item

    def bulk_update(self, items: model.QRCodes):
        session = self._mysql.get_session()
        session.bulk_update_mappings(items)
        session.commit()

    def list(self) -> model.QRCodes:
        qr_codes = self._mysql.get_session().query(model.QRCode).all()
        return qr_codes

    def list_qr_code_ids_by_feature(self, feature: model.QRCodeFeature) -> model.Ids:
        session = self._mysql.get_session()
        res = session.\
            query(model.QRCodeFeature.qr_code_id).\
            where(model.QRCodeFeature.feature == feature.feature).\
            where(model.QRCodeFeature.color == feature.color).\
            all()
        qr_code_ids = list(map(lambda item: item[0], res))
        return qr_code_ids

    def list_features(
        self,
        features: model.QRCodeFeatures
    ) -> model.QRCodeFeatures:
        cyan_feature_values: list[float] = []
        magenta_feature_values: list[float] = []
        yellow_feature_values: list[float] = []

        for feature in features:
            if feature.color == model.QRCodeFeatureColor.cyan:
                cyan_feature_values.append(feature.feature)
            elif feature.color == model.QRCodeFeatureColor.magenta:
                magenta_feature_values.append(feature.feature)
            elif feature.color == model.QRCodeFeatureColor.yellow:
                yellow_feature_values.append(feature.feature)

        session = self._mysql.get_session()
        qr_code_features = session.\
            query(model.QRCodeFeature). \
            filter(or_(
                and_(
                    model.QRCodeFeature.color == model.QRCodeFeatureColor.cyan,
                    model.QRCodeFeature.feature.in_(cyan_feature_values)
                ),
                and_(
                    model.QRCodeFeature.color == model.QRCodeFeatureColor.magenta,
                    model.QRCodeFeature.feature.in_(magenta_feature_values)
                ),
                and_(
                    model.QRCodeFeature.color == model.QRCodeFeatureColor.yellow,
                    model.QRCodeFeature.feature.in_(yellow_feature_values)
                )
            )).\
            all()
        return qr_code_features

    def add(self, s3_uri: str, file_name: str, features: model.QRCodeFeatures) -> model.QRCode:
        session = self._mysql.get_session()
        qr_code = model.QRCode(
            s3_uri=s3_uri,
            file_name=file_name
        )
        session.add(qr_code)
        session.flush()
        for feature in features:
            feature.qr_code_id = qr_code.id
        session.bulk_save_objects(features)
        session.commit()
        return qr_code

    def delete(self, qr_code_id):
        session = self._mysql.get_session()
        session.query(model.QRCode).filter(model.QRCode.id == qr_code_id).delete()
        session.query(model.QRCodeFeature).filter(model.QRCodeFeature.qr_code_id == qr_code_id).delete()
        session.commit()

    def list_by_is_feature_hash_cache_created(self, is_created: bool) -> model.QRCodes:
        session = self._mysql.get_session()
        qr_codes = session.\
            query(model.QRCode).\
            where(model.QRCode.is_feature_hash_cache_created == is_created).\
            all()
        return qr_codes

    def list_by_feature_hash_cache_created(self, feature_hash_cache_created: bool) -> model.QRCodes:
        session = self._mysql.get_session()
        qr_codes = session.\
            query(model.QRCode).\
            where(model.QRCode.feature_hash_cache_created == feature_hash_cache_created).\
            all()
        return qr_codes

    def list_qr_code_features_by_qr_code_is(self, qr_code_id) -> model.QRCodeFeature:
        session = self._mysql.get_session()
        features = session.\
            query(model.QRCodeFeature).\
            where(model.QRCodeFeature.qr_code_id == qr_code_id).\
            all()
        return features
