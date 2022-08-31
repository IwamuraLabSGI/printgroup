from PIL import Image
import sys
from domain.feature import get_features_from_img
from schema.mysql import MySQL, MySQLConfig
from repository.mysql.qr_code import QRCode as QRCodeRepo
from service.qr_code import QRCode as QRCodeSvc


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
    features = get_features_from_img(img)
    qr_code = qrCodeSvc.get_best_candidate(features)
    print(qr_code)







