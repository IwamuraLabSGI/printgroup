from schema.mysql import MySQL
import model.mysql as model
from sqlalchemy.dialects.mysql import insert

QRCodeFeatureHashCaches = list[model.QRCodeFeatureHashCache]
Hashes = list[float]

class QRCodeFeatureHashCache:
    _mysql: MySQL

    def __init__(self, mysql: MySQL):
        self._mysql = mysql

    def list_by_hashes(self, hashes: Hashes) -> QRCodeFeatureHashCaches:
        session = self._mysql.get_session()
        items = session.\
            query(model.QRCodeFeatureHashCache).\
            filter(model.QRCodeFeatureHashCache.hash.in_(hashes)).\
            all()
        return items

    def bulk_upsert(
            self,
            items_to_be_updated: QRCodeFeatureHashCaches,
            items_to_be_added: QRCodeFeatureHashCaches
    ):
        session = self._mysql.get_session()
        session.bulk_update_mappings(
            model.QRCodeFeatureHashCache,
            list(map(lambda item: item.__dict__, items_to_be_updated))
        )
        session.bulk_insert_mappings(
            model.QRCodeFeatureHashCache,
            list(map(lambda item: item.__dict__, items_to_be_added))
        )
        session.commit()

