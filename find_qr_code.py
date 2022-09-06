from datetime import datetime

from PIL import Image
import sys
from domain.feature import get_cmy_features_from_img
from schema.mysql import MySQL, MySQLConfig
from repository.mysql.qr_code import QRCode as QRCodeRepo
from service.qr_code import QRCode as QRCodeSvc
import model.mysql as model


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
qrCodeSvc = QRCodeSvc(qrCodeRepo)

args = sys.argv
with Image.open(args[1]) as img:
    start_time = datetime.now()

    cmy_features = get_cmy_features_from_img(img)

    cyan_features = list(map(lambda item: model.QRCodeFeature(
        feature=item,
        color=model.QRCodeFeatureColor.cyan
    ), cmy_features.get('cyan')))

    magenta_features = list(map(lambda item: model.QRCodeFeature(
        feature=item,
        color=model.QRCodeFeatureColor.magenta
    ), cmy_features.get('magenta')))

    yellow_features = list(map(lambda item: model.QRCodeFeature(
        feature=item,
        color=model.QRCodeFeatureColor.yellow
    ), cmy_features.get('yellow')))

    qr_code = qrCodeSvc.get_best_candidate_v2(
        cyan_features=cyan_features,
        magenta_features=magenta_features,
        yellow_features=yellow_features
    )

    if qr_code is None:
        print('Not found')
    else:
        print(qr_code.__dict__)

    time = datetime.now() - start_time
    print(f'time: {time}')







