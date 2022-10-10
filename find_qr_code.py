import collections
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

logs: list[str] = []
failed_files: list[str] = []
for file_path in target_file_paths:
    with Image.open(file_path) as img:
        start_time = datetime.now()

        qr_code_ids = qrCodeSvc.list_qr_code_ids_from_img(np.array(img, dtype=np.uint8))

        if len(qr_code_ids) == 0:
            print('Not found')
            logs.append(f'{file_path}: Not found')
        else:
            counter = collections.Counter(qr_code_ids)
            common = counter.most_common(10)
            found_qr_code_ids = [c[0] for c in common]
            found_qr_codes = list(map(lambda id: qrCodeSvc.get_by_id(id), found_qr_code_ids))
            found_qr_code_file_names = list(map(lambda qr_code: qr_code.file_name, found_qr_codes))

            file_id = int(os.path.splitext(os.path.basename(file_path))[0])
            best_qr_code_file_id = int(os.path.splitext(os.path.basename(found_qr_codes[0].file_name))[0])
            total_time = datetime.now() - start_time
            if file_id - 5000 != best_qr_code_file_id:
                failed_files.append(file_path)
                message = f'{file_id} Not match[{total_time}]: {found_qr_code_file_names}, {common}'
                print(message)
                logs.append(message)
            else:
                message = f'{file_id} Match[{total_time}]: {found_qr_code_file_names}, {common}'
                print(message)
                logs.append(message)

with open('dist/logs.txt', 'w') as f:
    f.write('\n'.join(logs))
with open('dist/failed.txt', 'w') as f:
    f.write('\n'.join(failed_files))
