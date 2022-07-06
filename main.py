from mysql import MySQL, MySQLConfig
from repository.mysql.qr_code import QRCode as QRCodeRepo
from service.qr_code import QRCode as QRCodeSvc
from llah.descriptor_extractor import DescriptorExtractor
import numpy as np
from llah.keypoint import Keypoint

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
qrCodeSvc.list()

descriptor_extractor = DescriptorExtractor(3)
keypoints = list(map(lambda _: Keypoint(np.random.rand(), np.random.rand(), np.random.rand()), range(1000)))
sampled_keypoints = descriptor_extractor.sample_keypoint(keypoints, 500)
print(len(sampled_keypoints))


