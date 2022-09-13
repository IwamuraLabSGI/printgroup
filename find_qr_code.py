import math
import os
from datetime import datetime

import numpy as np
from PIL import Image
import sys

import llah
import utils
from domain import CmykKeypointExtractor, FeatureCalculator
from repository.mysql.qr_code import QRCode as QRCodeRepo
from schema.mysql import load_mysql
from service.qr_code import QRCode as QRCodeSvc
import model.mysql as model


def sample_features(features: model.QRCodeFeatures) -> model.QRCodeFeatures:
    sample_total = 500
    sampled_features: model.QRCodeFeatures = []
    sample_span = math.floor(len(features) / sample_total)
    for i in range(sample_total):
        sampled_features.append(features[i * sample_span])
    return sampled_features


mysql = load_mysql()
mysql.connect()
qrCodeRepo = QRCodeRepo(mysql)
qrCodeSvc = QRCodeSvc(qrCodeRepo)

args = sys.argv
target_file_paths: list[str] = []
if os.path.isfile(args[1]):
    target_file_paths.append(args[1])
else:
    target_file_paths = utils.list_img_paths_in_dir(args[1])

search_result: list[str] = []
for file_path in target_file_paths:
    with Image.open(file_path) as img:
        start_time = datetime.now()

        qr_code = qrCodeSvc.find_qr_code(np.array(img, dtype=np.uint8))

        total_time = datetime.now() - start_time
        print(f'time: {total_time}')

        if qr_code is None:
            print('Not found')
            search_result.append(f'{file_path}: Not found')
        else:
            file_id = int(os.path.splitext(os.path.basename(file_path))[0])
            detected_file_id = int(os.path.splitext(os.path.basename(qr_code.file_name))[0])
            if file_id - 5000 != detected_file_id:
                print(f'Not match: {file_id} != {detected_file_id}')
                search_result.append(f'{file_path}: Not match: {file_id} != {detected_file_id}')
            else:
                print(f'Match: {file_id} == {detected_file_id}')


# search_resultをファイルに出力する
with open('dist/search_result.txt', 'w') as f:
    f.write('\n'.join(search_result))






