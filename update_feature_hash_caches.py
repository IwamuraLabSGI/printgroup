import math

from schema.mysql import MySQL, MySQLConfig
from repository.mysql.qr_code import QRCode as QRCodeRepo
from repository.mysql.qr_code_feature_hash_cache import QRCodeFeatureHashCache as QRCodeFeatureHashCacheRepo
from service.qr_code import QRCode as QRCodeSvc
import model.mysql as model


def get_hash_from_feature(feature: float):
    feature_decimal = math.modf(feature)[0]
    decimal_digit = 3
    floored_feature_decimal = math.floor(feature_decimal * (10**decimal_digit)) / (10**decimal_digit)
    return floored_feature_decimal


mysqlConfig = MySQLConfig(
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='qr_auth'
)

mysql = MySQL(mysqlConfig)
mysql.connect()
qrCodeRepo = QRCodeRepo(mysql)
qrCodeFeatureHashCacheRepo = QRCodeFeatureHashCacheRepo(mysql)
qrCodeSvc = QRCodeSvc(qrCodeRepo)

session = mysql.get_session()
qr_codes = qrCodeRepo.list_by_feature_hash_cache_created(False)

for qr_code in qr_codes:
    print(qr_code.id)
    qr_code_features = qrCodeRepo.list_qr_code_features_by_qr_code_is(qr_code.id)
    hashes = list(set(map(lambda item: get_hash_from_feature(item.feature), qr_code_features)))

    exist_items = qrCodeFeatureHashCacheRepo.list_by_hashes(hashes)

    items_to_be_updated: list[model.QRCodeFeatureHashCache] = []
    for exist_item in exist_items:
        # qr_code_idsが減るパターンは想定していない
        exist_item_qr_code_ids = exist_item.qr_code_ids
        exist_item_qr_code_ids.append(qr_code.id)
        unique_qr_code_ids = list(set(exist_item_qr_code_ids))
        exist_item.qr_code_ids = unique_qr_code_ids
        item_hashes_to_be_updated.append(exist_item.hash)
        items_to_be_updated.append(exist_item)

    item_hashes_to_be_updated = list(map(lambda item: item.hash, items_to_be_updated))
    item_hashes_to_be_added = list(filter(lambda hash: hash not in item_hashes_to_be_updated, hashes))
    items_to_be_added: list[model.QRCodeFeatureHashCache] = []
    for hash in item_hashes_to_be_added:
        items_to_be_added.append(model.QRCodeFeatureHashCache(
            hash=hash,
            qr_code_ids=[qr_code.id]
        ))

    qrCodeFeatureHashCacheRepo.bulk_upsert(items_to_be_updated, items_to_be_added)

    qr_code.feature_hash_cache_created = True
    qrCodeRepo.update(qr_code)
