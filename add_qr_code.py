import os.path

import cv2
import numpy as np
from PIL import Image
import sys

from appink import binarize_as_cmy
from schema.mysql import MySQL, MySQLConfig
from repository.mysql.qr_code import QRCode as QRCodeRepo
from service.qr_code import QRCode as QRCodeSvc
from domain.feature import get_cmy_features_from_img
import model.mysql as model

mysqlConfig = MySQLConfig(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='qr_auth'
)

mysql = MySQL(mysqlConfig)
mysql.connect()
qrCodeRepo = QRCodeRepo(mysql)
qrCodeSvc = QRCodeSvc(qrCodeRepo)

args = sys.argv
target_path = args[1]

target_file_paths: list[str] = []
if os.path.isfile(target_path):
    target_file_paths.append(target_path)
else:
    files_and_dirs = os.listdir(target_path)
    files = [item for item in files_and_dirs if os.path.isfile(os.path.join(target_path, item))]
    target_file_paths = list(map(lambda item: os.path.join(target_path, item), files))

for file_path in target_file_paths:
    print(f'add qr code: {file_path}')
    try:
        with Image.open(file_path) as img:
            cmy_features = get_cmy_features_from_img(img)
            # binarize_as_cmy(0, cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
            features: model.QRCodeFeatures = []
            for cmy_feature in cmy_features.get('cyan'):
                features.append(model.QRCodeFeature(
                    feature=cmy_feature,
                    color=model.QRCodeFeatureColor.cyan
                ))
            for cmy_feature in cmy_features.get('magenta'):
                features.append(model.QRCodeFeature(
                    feature=cmy_feature,
                    color=model.QRCodeFeatureColor.magenta
                ))
            for cmy_feature in cmy_features.get('yellow'):
                features.append(model.QRCodeFeature(
                    feature=cmy_feature,
                    color=model.QRCodeFeatureColor.yellow
                ))
            qrCodeSvc.add(
                file_name=os.path.basename(file_path),
                features=features
            )
    except Exception as e:
        print(e)
