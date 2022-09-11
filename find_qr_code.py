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

        cmy_keypoints = CmykKeypointExtractor.extract(np.array(img, dtype=np.uint8))

        descriptor_extractor = llah.DescriptorExtractor(6, 2)

        cyan_descriptors = descriptor_extractor.extract(cmy_keypoints.get('cyan'))
        magenta_descriptors = descriptor_extractor.extract(cmy_keypoints.get('magenta'))
        yellow_descriptors = descriptor_extractor.extract(cmy_keypoints.get('yellow'))

        cyan_features = list(map(lambda item: model.QRCodeFeature(
            feature=item,
            color=model.QRCodeFeatureColor.cyan
        ), FeatureCalculator.calc(cyan_descriptors)))

        magenta_features = list(map(lambda item: model.QRCodeFeature(
            feature=item,
            color=model.QRCodeFeatureColor.magenta
        ), FeatureCalculator.calc(magenta_descriptors)))

        yellow_features = list(map(lambda item: model.QRCodeFeature(
            feature=item,
            color=model.QRCodeFeatureColor.yellow
        ), FeatureCalculator.calc(yellow_descriptors)))

        qr_code = qrCodeSvc.get_best_candidate_v2(
            cyan_features=cyan_features,
            magenta_features=magenta_features,
            yellow_features=yellow_features
        )

        time = datetime.now() - start_time
        print(f'time: {time}')

        if qr_code is None:
            print('Not found')
            search_result.append(f'{file_path}: Not found')
        else:
            print(f'Found: {qr_code.file_name}, {qr_code.id}')
            search_result.append(f'{file_path}: {qr_code.file_name} [{time}]')


# search_resultをファイルに出力する
with open('dist/search_result.txt', 'w') as f:
    f.write('\n'.join(search_result))






