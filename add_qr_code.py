import os.path

import cv2
import numpy as np
from PIL import Image
import sys

from appink import binarize_as_cmy
from schema.mysql import MySQL, MySQLConfig
from repository.mysql.qr_code import QRCode as QRCodeRepo
from service.qr_code import QRCode as QRCodeSvc
from domain import Feature
import model.mysql as model
from utils.env import env

mysqlConfig = MySQLConfig(
    host=env('RDB_HOST'),
    port=env('RDB_PORT'),
    user=env('RDB_USER'),
    password=env('RDB_PASS'),
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
    with Image.open(file_path) as img:
        cmy_features = Feature.get_cmy_features_from_img(img)
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
